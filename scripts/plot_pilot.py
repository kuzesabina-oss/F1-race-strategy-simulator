from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/processed/bahrain_2024_clean_laps.csv")

colors = {"SOFT": "red", "HARD": "dimgray"}

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for compound, group in data.groupby("Compound"):
    color = colors.get(compound, "steelblue")

    # Все чистые круги: точка — один круг
    axes[0].scatter(
        group["tyre_age_laps"],
        group["lap_time_s"],
        alpha=0.25,
        s=18,
        color=color,
        label=compound,
    )

    # Медианное время отдельно для каждого возраста шин
    median_by_age = group.groupby("tyre_age_laps")["lap_time_s"].median()
    axes[1].plot(
        median_by_age.index,
        median_by_age.values,
        marker="o",
        markersize=3,
        color=color,
        label=compound,
    )

axes[0].set_title("Все круги")
axes[0].set_xlabel("Возраст комплекта шин (TyreLife, круги)")
axes[0].set_ylabel("Время круга (секунды)")
axes[0].legend(title="Compound")

axes[1].set_title("Медиана для каждого возраста шин")
axes[1].set_xlabel("Возраст комплекта шин (TyreLife, круги)")
axes[1].set_ylabel("Медианное время круга (секунды)")
axes[1].legend(title="Compound")

fig.suptitle("Bahrain 2024 — исследовательский график, не вывод модели")
fig.tight_layout()

output = Path("docs/bahrain_2024_tyre_age_eda.png")
fig.savefig(output, dpi=160)
print("Кругов на графике:", len(data))
print("График сохранён:", output)
