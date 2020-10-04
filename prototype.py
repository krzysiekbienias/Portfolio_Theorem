import numpy as np

x = np.random.normal(0, 1, 500)
y = np.random.normal(0, 1, 500)
X = np.vstack((x, y)).T

weight_array = []
for i in range(5):

        # Randomly assign floats to our 4 equities

        weights = np.random.random(5)

        # Convert the randomized floats to percentages (summing to 100)

        weights /= np.sum(weights)

        # Add to our portfolio weight array

        weight_array.append(weights)

print('the end')