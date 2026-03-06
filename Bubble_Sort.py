import time
import ast

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
         for j in range(0, n-1-i):
              if arr[j] > arr[j+1]:
                   arr[j], arr[j+1] = arr[j+1],arr[j]
    return arr

def selection_sort(arr):
     n = len(arr)
     for i in range(n):
          min_idx = i
          for j in range(i+1, n):
               if arr[j]< arr[min_idx]:
                    min_idx = j
                    arr[i], arr[min_idx] = arr[min_idx], arr[i]
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

print( bubble_sort([64, 34, 25, 12, 22, 11, 90]) )
print( selection_sort([64, 25, 12, 22, 11]) )
# Example: writing to a file
# output_filename = "FtimeBubSort.txt"

# with open(output_filename, 'w') as f:
#     f.write("This is the first line.\n")
#     f.write("This is the second line.\n")