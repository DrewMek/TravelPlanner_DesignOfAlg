import time
import ast

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
         for j in range(0, n-1-i):
              if arr[j][1] > arr[j+1][1]:
                arr[j], arr[j+1] = arr[j+1],arr[j]
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j][1] < arr[min_idx][1]: 
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
    
    bubblesort_results = []
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
        bubblesort_results.append(data_bubble)
        selectionsort_results.append(data_selection)
        runtime.append((bubble_time, selection_time))

        #print_to_file
    with open("FtimeBubSort.txt", "w") as f:
            for line in bubblesort_results:
                pairs = [(item[0], item[1]) for item in line]
                f.write(str(pairs) + "\n")

    with open("FtimeSelSort.txt", "w") as f:
            for line in selectionsort_results:
                pairs = [(item[0], item[1]) for item in line]
                f.write(str(pairs) + "\n")

    with open("runtimes.txt", "w") as f:
            for bub, sel in runtime:
                f.write(f"({bub}, {sel})\n")




if __name__ == "__main__":
     
    flight_sorting()