import matplotlib.pyplot as plt

# Define time points (days) for a 2-week iteration (14 days)
days = list(range(1, 15))  # 14-day iteration

# Ideal burndown line (evenly distributing 12 tasks over 14 days)
ideal_tasks_remaining = [12 - (i * 12 / 14) for i in range(14)]

# Actual burndown data based on the user's progress
actual_tasks_remaining = [12] * 5 + [6] * 4 + [3] * 3 + [0] * 2
# Plot the burndown chart
plt.figure(figsize=(10, 5))
plt.plot(days, ideal_tasks_remaining, label="Ideal Burndown", linestyle="dashed", color="blue")
plt.plot(days, actual_tasks_remaining, label="Actual Burndown", marker="o", color="red")

# Labels and title
plt.xlabel("Days")
plt.ylabel("Total Tasks")
plt.title("Burndown Chart for 2-week iteration")
plt.legend()
plt.grid(True)
plt.show()
