import numpy as np


def balance_2d_array(imbalanced_array):
    """Balances an imbalanced 2D array by length.

    Args:
        imbalanced_array (list): The imbalanced 2D array.

    Returns:
        list: The balanced 2D array.
    """
    # Calculate the target length for balanced arrays
    target_length = int(np.mean([len(arr) for arr in imbalanced_array]))

    # Initialize a list to store balanced arrays
    balanced_arrays = []

    # Initialize an array to store extra elements
    extra_elements = []

    # Iterate over the imbalanced arrays
    for arr in imbalanced_array:
        # Check if the array is longer than the target length
        if len(arr) > target_length:
            # Move elements from the longer array to the balanced array
            balanced_arrays.append(arr[:target_length])
            # Store the extra elements
            extra_elements.extend(arr[target_length:])
            print(extra_elements)
        else:
            # Append the array as is
            balanced_arrays.append(arr)
    for i in balanced_arrays:
        while len(i) < target_length and len(extra_elements) != 0:
            i.extend([extra_elements[-1]])
            extra_elements.pop()

    # Create additional arrays for the extra elements
    while len(extra_elements) > 0:
        # Create a new array and add elements from extra_elements
        new_array = extra_elements[:target_length]
        extra_elements = extra_elements[target_length:]
        balanced_arrays.append(new_array)

    return balanced_arrays


# Example imbalanced 2D array
imbalanced_array = [
    [1, 2, 3],
    [4, 5, 6, 7],
    [8, 9],
    [10, 11, 12, 13, 14],
    [15],
    [16, 17, 18, 19]
]

# Get the balanced array
balanced_array = balance_2d_array(imbalanced_array)

# Print the balanced array
print("Balanced Array:")
for arr in balanced_array:
    print(arr)
