from pathlib import Path
import fastf1

Path("data/cache").mkdir(parents=True, exist_ok=True)
Path("data/raw").mkdir(parents=True, exist_ok=True)

fastf1.Cache.enable_cache("data/cache")

session = fastf1.get_session(2024, "Bahrain", "R")
session.load(laps=True, telemetry=False, weather=False, messages=False)

laps = session.laps.copy()

print("Размер таблицы:", laps.shape)
print("Колонки:", laps.columns.tolist())
print(laps.head())

laps.to_csv("data/raw/bahrain_2024_laps.csv", index=False)
print("Сохранено: data/raw/bahrain_2024_laps.csv")
