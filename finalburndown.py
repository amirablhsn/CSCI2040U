import matplotlib.pyplot as plt

days = list(range(1, 43))

# Ideal burndown line (evenly distributing 12 tasks over 14 days)
ideal_tasks_remaining = [24 - (i * 24 / 42) for i in range(42)]

# Actual burndown data based on the user's progress
actual_tasks_remaining = [24] * 7 + [21] * 7 + [20] + [20] * 13 + [12] * 5 + [6] * 4 + [3] * 3 + [0] * 2

# Calculate velocity
tasks_completed_per_day = [actual_tasks_remaining[i] - actual_tasks_remaining[i+1] for i in range(41)]  # Compare consecutive days
total_tasks_completed = sum(tasks_completed_per_day)  # Sum all completed tasks
velocity = total_tasks_completed / len(tasks_completed_per_day)  # Average velocity over the iteration

# Plot the burndown chart
plt.figure(figsize=(10, 5))
plt.plot(days, ideal_tasks_remaining, label="Ideal Burndown", linestyle="dashed", color="blue")
plt.plot(days, actual_tasks_remaining, label="Actual Burndown", marker="o", color="red")

# Labels and title
plt.xlabel("Days")
plt.ylabel("Total Tasks")
plt.title(f"Burndown Chart for the entire project\nVelocity: {velocity:.2f} tasks per day")
plt.legend()
plt.grid(True)
plt.show()

# Print the velocity
print(f"Average Velocity: {velocity:.2f} tasks per day")
