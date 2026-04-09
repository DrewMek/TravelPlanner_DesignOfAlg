import time
import ast
import matplotlib.pyplot as plt

def bubble_sort(arr):
    n = len(arr)
    swaps = 0
    for i in range(n):
         for j in range(0, n-1-i):
              if arr[j][1] > arr[j+1][1]:
                arr[j], arr[j+1] = arr[j+1],arr[j]
                swaps = swaps + 1
    return arr, swaps

def selection_sort(arr):
    n = len(arr)
    swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j][1] < arr[min_idx][1]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, swaps

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
    bubble_swaps = []
    selection_swaps = []

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

        data_bubble, bubble_swaps_i = bubble_sort(data_bubble)

        BubTime_i = time.perf_counter_ns() - start

        # Selection Sort
        data_selection = original_list.copy()
        start = time.perf_counter_ns()
        data_selection, selection_swaps_i = selection_sort(data_selection)
        SelTime_i = time.perf_counter_ns() - start

        bubblesort_results.append(data_bubble)
        selectionsort_results.append(data_selection)
        bubble_swaps.append(bubble_swaps_i)
        selection_swaps.append(selection_swaps_i)
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

    print("Bubble Sort Swaps Per City:")
    for i, swaps in enumerate(bubble_swaps, start=1):
        print(f"City {i}: {swaps}")

    print("Total Bubble Sort Swaps:", sum(bubble_swaps))
    print("Total Selection Sort Swaps:", sum(selection_swaps))

# # Process cities.txt
# print("Cities:\n")

# try:
#     with open('cities.txt', 'r') as file:
#         for line in file:
#             print(line.strip())
# except FileNotFoundError:
#     print("Error: cities.txt not found.")

# ---------------------------------------------------------------------------
# PA3 related stuff
# ---------------------------------------------------------------------------

def load_cities(filepath='cities.txt'):
    """
    hi. This function reads cities.txt and returns a list of (city_id, x, y) tuples.
    Each line has the format id, x, ,y
    cities 1..max_i are used per call
    """
    cities = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.split()
            city_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
            cities.append((city_id, x, y))
    return cities


def euclidean_distance(city_a, city_b):
    """
    Returns the Euclidean distance between two cities.
    Each city is a tuple (id, x, y).
    Euclidean distance is just the straight line distance between two points.
    """
    # TODO: compute sqrt((x2-x1)^2 + (y2-y1)^2). look familiar?
    pass


def brute_force_closest(cities):
    """
    Brute Force closest pair (O(n^2)). ? fact check this
    Checks every pair of cities and returns (dist, city_a, city_b)
    for the pair with the smallest distance.
    """
    # TODO: brute force = nested loop over all pairs, keep track of minimum distance and the pair associated with that
    pass


def divide_and_conquer_closest(cities):
    """
    Divide-and-Conquer closest pair (O(n log n)).
    Entry point: sorts cities by x-coordinate, then calls dc_closest_rec.
    Returns (dist, city_a, city_b).
    """
    # TODO: sort by x, call dc_closest_rec, return result
    pass


def dc_closest_rec(sorted_by_x, sorted_by_y):
    """
    Recursive function for Divide-and-Conquer.
    Base case: if 3 points or less use brute force
    Recursive case:
        1. Split into left/right halves by median x
        2. Recurse on each half
        3. Take change = min(left_dist, right_dist)
        4. Build the strip of points within change of the dividing line
        5. Check strip pairs (should be at most 7 comparisons per point?)
        6. Return the overall minimum
    """
    # TODO: implement the logic shown above
    pass

#ignore all the hilbert stuff for now, let me deal with it

def run_closest_pair(cities_all):
    """
    For each i in {50, ..., 100}:
      - Runs brute_force_closest on cities[0:i]
      - Runs divide_and_conquer_closest on cities[0:i]
      - Runs hilbert_closest on cities[0:i]
      - Records runtimes (nanoseconds) via time.perf_counter_ns()
    Writes results to BF-Closest.txt, DC-Closest.txt, Hilbert-Closest.txt, and runtimes.txt.
    """
    bf_results = []
    dc_results = []
    h_results  = []
    runtimes   = []

    for i in range(50, 101):
        subset = cities_all[:i]

        start = time.perf_counter_ns()
        bf_results.append(brute_force_closest(subset))
        bf_time = time.perf_counter_ns() - start

        start = time.perf_counter_ns()
        dc_results.append(divide_and_conquer_closest(subset))
        dc_time = time.perf_counter_ns() - start

        start = time.perf_counter_ns()
        #h_results.append(hilbert_closest(subset))
        h_time = time.perf_counter_ns() - start

        runtimes.append((bf_time, dc_time, h_time))

    # each line: distance and the two city ids for that input size
    def fmt(result):
        dist, a, b = result
        return f"{dist:.6f} ({a[0]}, {b[0]})\n"

    with open('BF-Closest.txt', 'w') as f:
        for r in bf_results:
            f.write(fmt(r))

    with open('DC-Closest.txt', 'w') as f:
        for r in dc_results:
            f.write(fmt(r))

    #with open('Hilbert-Closest.txt', 'w') as f:
    #    for r in h_results:
    #        f.write(fmt(r))

    # runtimes.txt — line i-49 contains (BFTime_i, DCTime_i, HilbertTime_i)
    with open('runtimes.txt', 'w') as f:
        for bf_t, dc_t, h_t in runtimes:
            f.write(f"({bf_t}, {dc_t}, {h_t})\n")

    plot_closest_runtimes(runtimes)


def plot_closest_runtimes(runtimes):
    """
    plots brute and div and conq runtimes vs. number of cities (50..100).
    x-axis = number of cities, y-axis = clock time (nanoseconds).
    Saves the figure to closest_pair_runtime_plot.png.
    """
    # someone other than drew do this one because its quite shrimple to get the hang of, check documentation
    x = list(range(50, 101))
    bf_times = [r[0] for r in runtimes]
    dc_times = [r[1] for r in runtimes]
    h_times  = [r[2] for r in runtimes]

    plt.figure()
    plt.plot(x, bf_times, label="Brute Force")
    plt.plot(x, dc_times, label="Divide & Conquer")
    #plt.plot(x, h_times,  label="Hilbert Window")
    plt.xlabel("Number of Cities")
    plt.ylabel("Runtime (nanoseconds)")
    plt.title("Closest Pair Runtime Comparison")
    plt.legend()
    plt.savefig("closest_pair_runtime_plot.png")
    plt.show()


if __name__ == "__main__":
    flight_sorting()

    # Load cities and run closest-pair algorithms
    cities = load_cities('cities.txt')
    if cities:
        run_closest_pair(cities)