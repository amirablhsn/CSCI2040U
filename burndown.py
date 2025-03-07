import matplotlib.pyplot as plt

# Simulating an in-progress burn down chart for a 14-day sprint
in_progress_days = list(range(14))  # Full 14 days
in_progress_story_points = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0]  # Adjusted progress for 12 board items
ideal_in_progress_story_points = [12 - (12/13) * day for day in in_progress_days]  # Ideal trend line for 14-day sprint

# Plotting the in-progress burn down chart
plt.figure(figsize=(8,5))
plt.plot(in_progress_days, in_progress_story_points, marker='o', linestyle='-', color='red', label='Actual Progress')
plt.plot(in_progress_days, ideal_in_progress_story_points, linestyle='--', color='blue', label='Ideal Progress')

# Labels and title
plt.xlabel("Days")
plt.ylabel("Story Points Remaining")
plt.title("In-Progress Burn Down Chart (14-Day Sprint)")
plt.legend()
plt.grid(True)

# Show plot
plt.show()