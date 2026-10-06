from pathlib import Path

import pandas as pd

source = Path("data/raw/bahrain_2024_laps.csv")
output = Path("data/processed/bahrain_2024_clean_laps.csv")
audit_file = Path("docs/bahrain_2024_cleaning_audit.csv")

data = pd.read_csv(source)

rules = [
    ("LapTime есть", data["LapTime"].notna()),
    ("IsAccurate = True", data["IsAccurate"].eq(True)),
    ("TrackStatus = 1", data["TrackStatus"].astype(str).eq("1")),
    ("Нет PitInTime", data["PitInTime"].isna()),
    ("Нет PitOutTime", data["PitOutTime"].isna()),
    ("Compound заполнен", data["Compound"].notna()),
    ("TyreLife заполнен", data["TyreLife"].notna()),
    ("Deleted = False", data["Deleted"].eq(False)),
]

keep = pd.Series(True, index=data.index)
audit = [{"step": "Исходные строки", "rows_remaining": len(data)}]

for rule_name, condition in rules:
    keep &= condition.fillna(False)
    audit.append({
        "step": rule_name,
        "rows_remaining": int(keep.sum()),
    })

clean = data.loc[keep].copy()
clean["lap_time_s"] = pd.to_timedelta(
    clean["LapTime"], errors="coerce"
).dt.total_seconds()
clean["tyre_age_laps"] = clean["TyreLife"]

columns = [
    "Driver",
    "DriverNumber",
    "LapNumber",
    "Stint",
    "Compound",
    "tyre_age_laps",
    "lap_time_s",
    "TrackStatus",
    "Position",
]

output.parent.mkdir(parents=True, exist_ok=True)
audit_file.parent.mkdir(parents=True, exist_ok=True)

clean[columns].to_csv(output, index=False)
pd.DataFrame(audit).to_csv(audit_file, index=False)

print("Чистых кругов:", len(clean))
print("Составы шин:")
print(clean["Compound"].value_counts().to_string())
print("Сохранено:", output)
print("Журнал очистки:", audit_file)
