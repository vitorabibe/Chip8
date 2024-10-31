import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Constants from the datasheet (assuming the sensor's pressure range is 0 to 30 PSI)
P_min = 0
P_max = 30

# Function to convert the two-byte data into pressure bits (14-bit pressure)
def convert_to_pressure_bits(byte1, byte2):
    # Mask out the first 6 bits of byte1 and combine with byte2 to get the 14-bit value
    pressure_bits = ((byte1 & 0x3F) << 8) | byte2
    return pressure_bits

# Function to convert pressure bits to actual pressure (PSI)
def convert_to_pressure_psi(pressure_bits):
    pressure_psi = ((pressure_bits - 1638) / 13107) * (P_max - P_min) + P_min
    return pressure_psi

# Function to read the sensor data from a file and process it
def process_sensor_file(file_path):
    with open(file_path, 'r') as file:
        sensor_data = file.read()

    # Extract channel data using regex
    channels = re.findall(r"Channel #\d+ \[(\d+), (\d+)\]", sensor_data)

    # Process each channel's bytes to calculate pressure bits
    pressure_bits = []
    for channel in channels:
        byte1, byte2 = int(channel[0]), int(channel[1])
        pressure_bits.append(convert_to_pressure_bits(byte1, byte2))

    return pressure_bits

# Example usage:
# Replace 'sensor_readings.txt' with your actual file path
file_path = 'pitch-yaw-44-68.txt'
pressure_bits = process_sensor_file(file_path)

# Convert pressure bits to PSI
pressure_psi = [convert_to_pressure_psi(bits) for bits in pressure_bits]

# Assuming there are 7 channels in the dataset
num_channels = 7
channel_data = [[] for _ in range(num_channels)]
time_steps = []

# Store the pressure values in separate lists for each channel
for i in range(0, len(pressure_psi), num_channels):
    time_steps.append(i // num_channels)  # Simulating time or index for x-axis
    for j in range(num_channels):
        if i + j < len(pressure_psi):
            channel_data[j].append(pressure_psi[i + j])

# Plot each channel on a different graph with a best-fit curve
fig, axes = plt.subplots(num_channels, 1, figsize=(8, 15))

for channel_idx in range(num_channels):
    df = pd.DataFrame({'Time': time_steps, 'Pressure (PSI)': channel_data[channel_idx]})

    # Fit a polynomial model to the data (degree 2)
    model = np.poly1d(np.polyfit(df['Time'], df['Pressure (PSI)'], 2))
    
    # Generate a range of x values for plotting the fitted curve
    polyline = np.linspace(min(df['Time']), max(df['Time']), 250)
    
    # Plot scatter plot and the polynomial fit
    axes[channel_idx].scatter(df['Time'], df['Pressure (PSI)'], label=f"Channel {channel_idx + 1}")
    axes[channel_idx].plot(polyline, model(polyline), color='red', label=f"Best Fit Curve (Channel {channel_idx + 1})")
    
    # Set labels and title for each subplot
    axes[channel_idx].set_xlabel("Time (or index)")
    axes[channel_idx].set_ylabel("Pressure (PSI)")
    axes[channel_idx].set_title(f"Pressure Readings - Channel {channel_idx + 1}")
    axes[channel_idx].legend()

# Adjust layout for readability
plt.tight_layout()
plt.show()

# Print the pressure readings in PSI
print(pressure_psi)
