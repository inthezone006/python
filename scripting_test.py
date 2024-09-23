import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from CSV file
df_4000 = pd.read_csv('6x6_InP_bands.csv')

# Assuming the CSV file has 'x' and 'y' columns
x_4000 = df_4000['x']
y_4000 = df_4000['y']

# Load the 600 points from a .dat file
# Assuming the .dat file has two columns (x and y) and space or tab-separated values
data_600 = np.loadtxt('InP_4x4_50_elem_120_Ek.dat')  # Adjust delimiter if necessary
x_600 = data_600[:, 0]
y_600 = data_600[:, 1]

# Get the range of x-values from the 600-point dataset
x_min_600 = np.min(x_600)
x_max_600 = np.max(x_600)

# Filter the 4000-point dataset to include only x-values within the range of the 600-point dataset
x_4000_filtered = x_4000[(x_4000 >= x_min_600) & (x_4000 <= x_max_600)]
y_4000_filtered = y_4000[(x_4000 >= x_min_600) & (x_4000 <= x_max_600)]

# Check if there are any points in the 4000-point dataset within the range
if len(x_4000_filtered) == 0:
    print("No x-values from the 4000-point dataset fall within the range of the 600-point dataset.")
else:
    # Compare points that are within the range
    accuracy_list = []
    
    # Loop over the x-values from the 600-point dataset
    for i, x_val_600 in enumerate(x_600):
        # Find the y-values from the filtered 4000-point dataset that are closest to the current x_val_600
        y_vals_4000_in_range = y_4000_filtered[np.abs(x_4000_filtered - x_val_600).argmin()]

        # Compare the y-values for the current x_val_600 and corresponding y-values from the 4000-point dataset
        y_vals_600 = y_600[i]
        
        # Ensure that y-values are valid (non-empty)
        if len(np.array([y_vals_4000_in_range])) > 0:
            mean_diff = np.mean(np.abs(y_vals_600 - y_vals_4000_in_range))

            # Check for division by zero and ensure valid accuracy calculation
            if np.max(y_vals_600) != 0:
                accuracy = 1 - (mean_diff / np.max(y_vals_600))  # Normalize the accuracy
                accuracy_list.append(accuracy)
            else:
                accuracy_list.append(0)  # Handle edge case of max(y_vals_600) being 0
        else:
            accuracy_list.append(0)  # Handle case where y-values are empty or missing

    # Plot the comparison
    plt.figure(figsize=(10, 6))
    plt.plot(x_4000_filtered, y_4000_filtered, 'ro', alpha=0.5, label='4000-point dataset')
    plt.plot(x_600, y_600, 'bo', alpha=0.5, label='600-point dataset')

    plt.title('Comparison of MS_basis_final_Ek_reduced vs. InAs_4x4_square within x range')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

    # Calculate and print mean accuracy on a 0-5 scale if there are valid accuracy values
    if len(accuracy_list) > 0:
        mean_accuracy = np.mean(accuracy_list) * 100  # Convert to percentage
        mean_accuracy_0_5_scale = 5 - (mean_accuracy / 20)  # Transform to 0-5 scale
        print(f'Mean accuracy on 0-5 scale: {mean_accuracy_0_5_scale:.2f}')
    else:
        print("No valid accuracy values could be calculated.")
