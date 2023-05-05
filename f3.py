'''
Created on May 3, 2023

@author: yanyo
'''
import matplotlib.pyplot as plt
import numpy as np

# Generate some sample data
x = ['A', 'B', 'C', 'D', 'E']
y1 = [10, 8, 6, 4, 2]
y2 = [6, 8, 10, 12]
x3 = ['B', 'C', 'D', 'E']

# Set the width of the bars
width = 0.4

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the first bar chart
ax.bar(x, y1, width, label='Data 1')

# Shift the x-coordinates of the bars to the right
x2 = [i + width+1 for i in range(len(x3))]

# Plot the second bar chart
ax.bar(x2, y2, width, label='Data 2')

# Add a title and labels to the plot
ax.set_title('Bar Chart Comparison')
ax.set_xlabel('Category')
ax.set_ylabel('Value')

# Add a legend to the plot
ax.legend()

# Show the plot
plt.show()
