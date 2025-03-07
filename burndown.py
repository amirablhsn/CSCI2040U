import matplotlib.pyplot as plt

# Simulating an in-progress burn down chart (only halfway through the sprint)
in_progress_days = list(range(8))  # Days from 0 to 7 (halfway point)
in_progress_story_points = [100, 90, 85, 75, 70, 60, 50, 45]  # Progress so far
ideal_in_progress_story_points = [100 - (100/13) * day for day in in_progress_days]  # Ideal trend line

# Plotting the in-progress burn down chart
plt.figure(figsize=(8,5))
plt.plot(in_progress_days, in_progress_story_points, marker='o', linestyle='-', color='red', label='Actual Progress')
plt.plot(in_progress_days, ideal_in_progress_story_points, linestyle='--', color='blue', label='Ideal Progress')

# Labels and title
plt.xlabel("Days")
plt.ylabel("Story Points Remaining")
plt.title("In-Progress Burn Down Chart")
plt.legend()
plt.grid(True)

# Show plot
plt.show()
