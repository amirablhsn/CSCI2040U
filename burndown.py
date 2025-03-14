import matplotlib.pyplot as plt

# Define time points (days) for iterations
days = list(range(1, 29))  # 28-day iteration

# Ideal burndown line (evenly distributing 12 tasks over 28 days)
ideal_tasks_remaining = [12 - (i * 12 / 28) for i in range(28)]

# Actual burndown data based on the user's progress
actual_tasks_remaining = [12] * 7 + [9] * 7 + [8] + [8] * 13  # Updated with given progress

# Plot the burndown chart
plt.figure(figsize=(10, 5))
plt.plot(days, ideal_tasks_remaining, label="Ideal Burndown", linestyle="dashed", color="blue")
plt.plot(days, actual_tasks_remaining, label="Actual Burndown", marker="o", color="red")

# Labels and title
plt.xlabel("Days")
plt.ylabel("Total Tasks")
plt.title("Burndown Chart for 2 week iteration")
plt.legend()
plt.grid(True)
plt.show()
