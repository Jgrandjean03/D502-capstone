"""Step 7: build features, chronological split, two logistic regression rows, evaluation and exports."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_recall_curve, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

TRAIN_MAX_UDI = 7900
TEST_MIN_UDI = 8001
CUTOFF = 0.5
TXT_PATH = Path("outputs/07_models.txt")
CURVES_PATH = Path("outputs/07_pr_curves.csv")
CLEANED_PATH = Path("outputs/07_cleaned_dataset.csv")

engine = create_engine("postgresql+psycopg:///ai4i")
df = pd.read_sql("SELECT * FROM ai4i ORDER BY udi", engine)

decimals = ["air_temp_k", "process_temp_k", "torque_nm"]
df[decimals] = df[decimals].astype(float)

df["type_m"] = (df["type"] == "M").astype(int)
df["type_h"] = (df["type"] == "H").astype(int)
df["power_w"] = df["torque_nm"] * df["rot_speed_rpm"] * 2 * np.pi / 60
df["temp_diff_k"] = df["process_temp_k"] - df["air_temp_k"]
df["wear_x_torque"] = df["tool_wear_min"] * df["torque_nm"]

raw = ["air_temp_k", "process_temp_k", "rot_speed_rpm", "torque_nm", "tool_wear_min", "type_m", "type_h"]
engineered = raw + ["power_w", "temp_diff_k", "wear_x_torque"]

train = df[df["udi"] <= TRAIN_MAX_UDI]
test = df[df["udi"] >= TEST_MIN_UDI]
y_train = train["machine_failure"]
y_test = test["machine_failure"]

lines = [
    f"Train rows: {len(train)}, failures: {y_train.sum()}",
    f"Test rows: {len(test)}, failures: {y_test.sum()}",
    f"Training failures per input (10 inputs): {y_train.sum() / len(engineered):.1f}",
    "",
]

curves = []
for name, cols in [("row 1 raw", raw), ("row 2 engineered", engineered)]:
    scaler = StandardScaler().fit(train[cols])
    model = LogisticRegression(class_weight="balanced", max_iter=1000)
    model.fit(scaler.transform(train[cols]), y_train)
    scores = model.predict_proba(scaler.transform(test[cols]))[:, 1]
    alerts = (scores >= CUTOFF).astype(int)
    lines += [
        f"{name} ({len(cols)} inputs)",
        f"  PR-AUC (average precision): {average_precision_score(y_test, scores):.4f}",
        f"  Precision at {CUTOFF}: {precision_score(y_test, alerts):.4f}",
        f"  Recall at {CUTOFF}: {recall_score(y_test, alerts):.4f}",
        f"  Alerts: {alerts.sum()}, caught: {(alerts & y_test.to_numpy()).sum()}",
    ]
    precision, recall, _ = precision_recall_curve(y_test, scores)
    curves.append(pd.DataFrame({"model": name, "recall": recall, "precision": precision}))

rule_flags = test[["twf", "hdf", "pwf", "osf"]].sum(axis=1)
unflagged = ((y_test == 1) & (rule_flags == 0)).sum()
lines += [
    "",
    f"No-skill PR-AUC floor (test failure rate): {y_test.mean():.4f}",
    "Always 'no failure' recall: 0",
    f"Test failures with no rule flag: {unflagged}",
    f"Recall ceiling: {1 - unflagged / y_test.sum():.4f}",
]

pd.concat(curves).to_csv(CURVES_PATH, index=False)
df.drop(columns=["type_m", "type_h"]).to_csv(CLEANED_PATH, index=False)

report = "\n".join(lines) + "\n"
TXT_PATH.write_text(report)
print(report)
