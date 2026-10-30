race_laps = 30
base_lap_time = 90
pit_stop_time = 22
tire_degradation = {
  "soft" : 0.12,
  "medium" : 0.07,
  "hard" : 0.04
}

strategy_1 = {
  "stops" : [15],
  "tires" : ["medium" , "hard"]
}
strategy_2 = {
  "stops" : [10, 20],
  "tires" : ["soft","medium","soft"]
}

def simulate_strategy(strategy):
    total_time = 0

    stops = strategy["stops"]
    tires = strategy["tires"]

    stint_boundaries = [0] + stops + [race_laps]

    for i in range(len(tires)):
        tire = tires[i]

        start_lap = stint_boundaries[i]
        end_lap = stint_boundaries[i + 1]

        degradation = tire_degradation[tire]

        for lap in range(end_lap - start_lap):
            lap_time = base_lap_time + degradation * lap
            total_time += lap_time

        if i < len(stops):
            total_time += pit_stop_time

    return total_time


time_1 = simulate_strategy(strategy_1)
time_2 = simulate_strategy(strategy_2)

print("Strategy 1:", time_1, "seconds")
print("Strategy 2:", time_2, "seconds")

if time_1 < time_2:
    print("Strategy 1 is faster!")
else:
    print("Strategy 2 is faster!")
