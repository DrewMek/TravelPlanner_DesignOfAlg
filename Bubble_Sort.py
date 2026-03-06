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
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]: 
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
    bublesort_results = []
    selectionsort_results = []
    runtime = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
             data = ast.literal_eval(line)
             original_list = [list(item) for item in data]
        except (ValueError, SyntaxError) as e:
             print(f"Error parsing line: {line}\n{e}")
             continue
        
        # Bubble Sort
        data_bubble = [item for item in original_list]
        start_bubble = time.perf_counter_ns()
        bubble_sort(data_bubble)
        bubble_time = time.perf_counter_ns() - start_bubble

        # Selection Sort
        data_selection = [item for item in original_list]
        start_selection = time.perf_counter_ns()
        selection_sort(data_selection)
        selection_time = time.perf_counter_ns() - start_selection

        #Results
        bubble_sort.append(data_bubble)
        selection_sort.append(data_selection)
        runtime.append((bubble_time, selection_time))

        #print_to_file
    with open("FtimeBubSort.txt", 'w') as f:
         for i in range(len(bubble_sort)):
              

print("\n")  # spacing


# # Process cities.txt
# print("Cities:\n")

# try:
#     with open('cities.txt', 'r') as file:
#         for line in file:
#             print(line.strip())
# except FileNotFoundError:
#     print("Error: cities.txt not found.")

if __name__ == "__main__":
     
    # print( bubble_sort([64, 34, 25, 12, 22, 11, 90]) )

    # print("\n")  # spacing
    # print("Selection Sort:\n")
    # print( selection_sort([64, 25, 12, 22, 11, 34, 90]) )
# Example: writing to a file
# output_filename = "FtimeBubSort.txt"

# with open(output_filename, 'w') as f:
#     f.write("This is the first line.\n")
#     f.write("This is the second line.\n")