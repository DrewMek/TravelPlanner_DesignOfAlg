import time
import ast

def bubble_sort(arr):
    return arr

def selection_sort(arr):
     return arr

# Process flights.txt
def flight_sorting():
    try:
            with open('flights.txt', 'r') as f:
                lines = f.readlines()
    except FileNotFoundError:
            print("Error: 'flights.txt' not found in the current directory.")
            return


print("\n")  # spacing


# Process cities.txt
print("Cities:\n")

try:
    with open('cities.txt', 'r') as file:
        for line in file:
            print(line.strip())
except FileNotFoundError:
    print("Error: cities.txt not found.")


# Example: writing to a file
# output_filename = "FtimeBubSort.txt"

# with open(output_filename, 'w') as f:
#     f.write("This is the first line.\n")
#     f.write("This is the second line.\n")