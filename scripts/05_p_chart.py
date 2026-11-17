"""Step 5: p-chart of failure rate (25 groups of 400 rows in udi order)."""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

GROUP_SIZE = 400
CSV_PATH = Path("outputs/05_p_chart_groups.csv")
TXT_PATH = Path("outputs/05_p_chart.txt")

engine = create_engine("postgresql+psycopg:///ai4i")
df = pd.read_sql("SELECT udi, machine_failure FROM ai4i ORDER BY udi", engine)

df["group"] = (df["udi"] - 1) // GROUP_SIZE + 1
groups = df.groupby("group")["machine_failure"].agg(["count", "sum"])
groups = groups.rename(columns={"count": "rows", "sum": "failures"})

p_bar = groups["failures"].sum() / groups["rows"].sum()
sigma = (p_bar * (1 - p_bar) / GROUP_SIZE) ** 0.5
lcl = p_bar - 3 * sigma
ucl = p_bar + 3 * sigma

groups["rate"] = groups["failures"] / groups["rows"]
groups["outside"] = (groups["rate"] < lcl) | (groups["rate"] > ucl)
groups["center"] = p_bar
groups["lcl"] = lcl
groups["ucl"] = ucl
groups.to_csv(CSV_PATH)

summary = [
    f"Groups: {len(groups)} of {GROUP_SIZE} rows",
    f"Center line: {p_bar:.4f}",
    f"Sigma: {sigma:.6f}",
    f"Lower limit: {lcl:.4f}",
    f"Upper limit: {ucl:.4f}",
    f"Groups outside limits: {list(groups.index[groups['outside']])}",
]
report = "\n".join(summary) + "\n"
TXT_PATH.write_text(report)
print(report)
