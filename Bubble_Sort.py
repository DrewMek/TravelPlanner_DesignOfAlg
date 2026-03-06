import time
import ast
import matplotlib.pyplot as plt

#Credit statment: Oliver Conley, Dre Meketi, Ty Madsen

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
    BubTime = []
    SelTime = []

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
        data_bubble = original_list.copy()
        start = time.perf_counter_ns()
        bubble_sort(data_bubble)
        BubTime_i = time.perf_counter_ns() - start

        # Selection Sort
        data_selection = original_list.copy()
        start = time.perf_counter_ns()
        selection_sort(data_selection)
        SelTime_i = time.perf_counter_ns() - start

        bubblesort_results.append(data_bubble)
        selectionsort_results.append(data_selection)

        BubTime.append(BubTime_i)
        SelTime.append(SelTime_i)

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
        for i in range(len(BubTime)):
            f.write(f"({BubTime[i]}, {SelTime[i]})\n")

    x = list(range(1, len(BubTime) + 1))
    #simply plots times against each run of bubble and selection sort
    plt.plot(x, BubTime, label="Bubble Sort")
    plt.plot(x, SelTime, label="Selection Sort")

    #not part of data, just naming
    plt.xlabel("City Index (Line Number)")
    plt.ylabel("Runtime (nanoseconds)")
    plt.title("Bubble Sort vs Selection Sort Runtime")

    plt.legend()

    plt.savefig("runtime_plot.png")
    plt.show()

if __name__ == "__main__":
    flight_sorting()