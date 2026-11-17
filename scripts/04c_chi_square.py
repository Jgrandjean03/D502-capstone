"""Step 4c: chi-square test of failure rate by product variant (L, M, H)."""
from pathlib import Path

import pandas as pd
from scipy.stats import chi2_contingency
from sqlalchemy import create_engine

OUT_PATH = Path("outputs/04c_chi_square.txt")
ALPHA = 0.05
GAP_THRESHOLD_PP = 1.0

engine = create_engine("postgresql+psycopg:///ai4i")
df = pd.read_sql("SELECT type, machine_failure FROM ai4i", engine)

observed = pd.crosstab(df["type"], df["machine_failure"]).reindex(["L", "M", "H"])

chi2, p_value, dof, expected = chi2_contingency(observed)
expected = pd.DataFrame(expected, index=observed.index, columns=observed.columns)

rates_pct = 100 * observed[1] / observed.sum(axis=1)
gap_pp = rates_pct.max() - rates_pct.min()

n = observed.to_numpy().sum()
k = min(observed.shape)
cramers_v = (chi2 / (n * (k - 1))) ** 0.5

lines = [
    "Observed counts (0 = no failure, 1 = failure):",
    observed.to_string(),
    "",
    "Expected counts if all variants had the same failure rate:",
    expected.round(2).to_string(),
    f"Smallest expected count: {expected.to_numpy().min():.4f}",
    f"Every expected count at least 5: {bool((expected >= 5).all().all())}",
    "",
    "Failure rate by variant (%):",
    rates_pct.round(3).to_string(),
    "",
    f"Chi-square statistic: {chi2:.4f}",
    f"Degrees of freedom: {dof}",
    f"p-value: {p_value:.6f}",
    f"Reject null at alpha {ALPHA}: {p_value < ALPHA}",
    f"Cramer's V: {cramers_v:.4f}",
    f"Highest rate: {rates_pct.idxmax()}; lowest rate: {rates_pct.idxmin()}",
    f"Gap (percentage points): {gap_pp:.3f}",
    f"Gap at least {GAP_THRESHOLD_PP} point: {gap_pp >= GAP_THRESHOLD_PP}",
]

report = "\n".join(lines) + "\n"
OUT_PATH.write_text(report)
print(report)
