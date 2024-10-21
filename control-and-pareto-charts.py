import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Simulating some response times (in milliseconds) for help desk ticket resolution
np.random.seed(42)  # For reproducibility
num_samples = 25
response_times = np.random.normal(loc=300, scale=50, size=num_samples)

# Calculate the process average (mean) and control limits (3-sigma limits)
mean = np.mean(response_times)
std_dev = np.std(response_times)
ucl = mean + 3 * std_dev  # Upper Control Limit (mean + 3 * standard deviation)
lcl = mean - 3 * std_dev  # Lower Control Limit (mean - 3 * standard deviation)

# Plotting the control chart
plt.figure(figsize=(10, 6))
plt.plot(response_times, marker='o', linestyle='-', color='b', label='Response Times')
plt.axhline(mean, color='green', linestyle='--', label=f'Mean ({mean:.2f} ms)')
plt.axhline(ucl, color='red', linestyle='--', label=f'UCL ({ucl:.2f} ms)')
plt.axhline(lcl, color='red', linestyle='--', label=f'LCL ({lcl:.2f} ms)')

# Highlight points outside the control limits
out_of_control = np.where((response_times > ucl) | (response_times < lcl))[0]
plt.scatter(out_of_control, response_times[out_of_control], color='red', zorder=5, label='Out of Control')

plt.title('Control Chart - Help Desk Ticket Response Times')
plt.xlabel('Sample Number')
plt.ylabel('Response Time (ms)')
plt.legend()
plt.grid(True)
plt.show()

# Categorizing response times into 'issue types' based on thresholds
issue_types = {
    'Slow Response (250-300ms)': np.sum((response_times >= 250) & (response_times < 300)),
    'Very Slow Response (300-350ms)': np.sum((response_times >= 300) & (response_times < 350)),
    'Extremely Slow Response (>350ms)': np.sum(response_times >= 350),
    'Under 250ms': np.sum(response_times < 250)
}

# Creating a DataFrame from issue types
pareto_data = pd.DataFrame(list(issue_types.items()), columns=['Issue Type', 'Frequency'])

# Sort the data by frequency
pareto_data = pareto_data.sort_values(by='Frequency', ascending=False)

# Cumulative percentage for the line chart
pareto_data['Cumulative Percentage'] = pareto_data['Frequency'].cumsum() / pareto_data['Frequency'].sum() * 100

# Plot the Pareto Chart
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar chart (frequencies)
bars = ax1.bar(pareto_data['Issue Type'], pareto_data['Frequency'], color='blue')
ax1.set_ylabel('Frequency')
ax1.set_xlabel('Issue Type')

# Line chart (cumulative percentage)
ax2 = ax1.twinx()
line = ax2.plot(pareto_data['Issue Type'], pareto_data['Cumulative Percentage'], color='green', marker='o', linestyle='-')
ax2.set_ylabel('Cumulative Percentage')

# Adding threshold lines for 80% rule
ax2.axhline(80, color='red', linestyle='--', label='80% Threshold')

# Rotate x-axis labels to avoid overlap
plt.xticks(rotation=45, ha='right')

# Adding space to avoid label overlap
plt.tight_layout()

# Title and legend
plt.title('Pareto Chart - Help Desk Response Times')
ax2.legend(loc='lower right')

# Display the plot
plt.show()
