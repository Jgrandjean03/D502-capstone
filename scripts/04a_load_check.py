"""Step 4a: confirm the PostgreSQL table loads in pandas and the CSV is in UDI order."""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = Path("data/raw/ai4i2020.csv")
OUT_PATH = Path("outputs/04a_load_check.txt")

engine = create_engine("postgresql+psycopg:///ai4i")
table = pd.read_sql("SELECT * FROM ai4i", engine)

raw = pd.read_csv(CSV_PATH)
udi = raw["UDI"]
in_order = udi.tolist() == list(range(1, 10001))

lines = [
    f"Table rows: {table.shape[0]}",
    f"Table columns: {table.shape[1]}",
    f"CSV rows: {raw.shape[0]}",
    f"CSV first UDI: {udi.iloc[0]}",
    f"CSV last UDI: {udi.iloc[-1]}",
    f"CSV UDI runs 1 to 10000 in file order with no gaps: {in_order}",
]

report = "\n".join(lines) + "\n"
OUT_PATH.write_text(report)
print(report)
