import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define the screen dimensions
screen_width = 1920
screen_height = 1080

# Define the no-click zones as given
no_click_zones = [
    (0, 0, 500, 260),
    (800, 0, 1920, 100),
    (1300, 100, 1920, 270),
    (0, 950, 1920, 1080),
    (1600, 888, 1920, 1080),
    (5, 0, 5, 1080)
]

# Create a plot
fig, ax = plt.subplots()

# Set the dimensions of the plot to match the screen dimensions
ax.set_xlim(0, screen_width)
ax.set_ylim(0, screen_height)
ax.set_aspect(1)

# Plot the no-click zones
for zone in no_click_zones:
    x1, y1, x2, y2 = zone
    width = x2 - x1
    height = y2 - y1
    rect = patches.Rectangle((x1, screen_height - y2), width, height, linewidth=1, edgecolor='r', facecolor='r', alpha=0.5)
    ax.add_patch(rect)

# Set labels and title
ax.set_xlabel('Width (pixels)')
ax.set_ylabel('Height (pixels)')
ax.set_title('No-Click Zones Visualization')

# Display the plot
plt.gca().invert_yaxis()
plt.show()
