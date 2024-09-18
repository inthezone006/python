import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from CSV file
df_4000 = pd.read_csv('AlAs_4x4.csv')

# Assuming the CSV file has 'x' and 'y' columns
x_4000 = df_4000['x']
y_4000 = df_4000['y']

# Load the 600 points from a .dat file
# Assuming the .dat file has two columns (x and y) and space or tab-separated values
data_600 = np.loadtxt('MS_basis_final_Ek_reduced.dat')  # Adjust delimiter if necessary
x_600 = data_600[:, 0]
y_600 = data_600[:, 1]

# Find the indices of the matching x-values from the 600-point dataset in the 4000-point dataset
indices_4000 = [np.argmin(np.abs(x_4000 - x)) for x in x_600]

# Extract the corresponding y-values from the 4000-point file for each x in 600 points
y_4000_selected = []
for idx in indices_4000:
    # Here we collect all y-values for the matching x in the 4000-point dataset
    x_val = x_4000.iloc[idx]
    y_vals_at_x = df_4000[df_4000['x'] == x_val]['y'].values
    y_4000_selected.append(y_vals_at_x)

# Calculate the accuracy by comparing multiple y-values at each x
accuracy_list = []
for i, y_vals_4000 in enumerate(y_4000_selected):
    y_vals_600 = data_600[data_600[:, 0] == x_600[i], 1]
    
    # Here, we can compare the mean or median or use some other method to find accuracy
    mean_diff = np.mean(np.abs(np.mean(y_vals_600) - np.mean(y_vals_4000)))
    accuracy = 1 - (mean_diff / np.max(y_vals_600))  # Normalize the accuracy
    accuracy_list.append(accuracy)

# Plot the comparison
plt.figure(figsize=(10, 6))
for i, y_vals_4000 in enumerate(y_4000_selected):
    plt.plot([x_600[i]] * len(y_vals_4000), y_vals_4000, 'ro', alpha=0.5)
    plt.plot([x_600[i]] * len(y_vals_600), y_vals_600, 'bo', alpha=0.5)

plt.title('Comparison of MS_basis_final_Ek_reduced vs. AlAs_4x4 with multiple y values')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend(['AlAs_4x4', 'MS_basis_final_Ek_reduced'])
plt.show()

# Calculate and print mean accuracy on a 0-5 scale
mean_accuracy = np.mean(accuracy_list) * 100  # Convert to percentage
mean_accuracy_0_5_scale = 5 - (mean_accuracy / 20)  # Transform to 0-5 scale

print(f'Mean accuracy on 0-5 scale: {mean_accuracy_0_5_scale:.2f}')
