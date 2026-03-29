import time
import matplotlib.pyplot as plt

# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    if len(arr) > 1:
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i][1] < right[j][1]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        return result + left[i:] + right[j:]

#Quick Sort Lomuto
def quick_sort_Lomuto(arr, low, high):
    def qsort(arr, low, high):
        if low < high:
            p = partition(arr, low, high)
            qsort(arr, low, p - 1)
            qsort(arr, p + 1, high)
    
    # Lomuto partition scheme
    def partition(arr, low, high):
        pivot = arr[high][1]
        i = low - 1
        for j in range(low, high):
            if arr[j][1] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    qsort(arr, low, high)
    return arr

#quick Sort Hoare
def quick_sort_Hoare(arr, low, high):
    def qsort(arr, low, high):
        if low < high:
            p = partition(arr, low, high)
            qsort(arr, low, p)
            qsort(arr, p + 1, high)
    
    # Hoare partition scheme
    def partition(arr, low, high):
        pivot = arr[low][1]
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while arr[i][1] < pivot:
                i += 1
            j -= 1
            while arr[j][1] > pivot:
                j -= 1
            if i >= j:
                return j
            arr[i], arr[j] = arr[j], arr[i]
    qsort(arr, low, high)
    return arr

#Sorted Files
sorted_files = {
    "merge_sort" : "cost_MerSort.txt",
    "lomuto" : "cost_QSortLom.txt", 
    "hoare" : "cost_QSortHoare.txt"
}

with open("round2_output.txt", "w") as f:
    lines = f.readlines()

#Trips with budget of 5000
B = 5000
trip_numbers = []

#using the sorted lists to find the trips that are under the budget
for city_list in sorted_files["merge"]:
    total_cost = 0
    count = 0

    for city, cost in city_list:
        if total_cost + cost <= B:
            total_cost += cost
            count += 1
        else:
            break
    trip_numbers.append(count)

#write the trip numbers to file
with open("trip_numbers.txt", "w") as f:
    for num in trip_numbers:
        f.write(str(num) + "\n")

#stored sorted data
sorted_lists = {"merge": [], "lomuto": [], "hoare": []}
runtime = []

for idx, line in enumerate(lines):
    pairs = line.split()

    #make touples
    cities = [(int(pairs[i]), float(pairs[i + 1])) for i in range(0, len(pairs), 2)]

    #merge sort time
    start = time.time_ns()
    merge_sorted = merge_sort(cities)
    merge_time = time.time_ns() - start
    sorted_lists["merge"].append(merge_sorted)

    #quick sort lomuto time
    start = time.time_ns()
    lomuto_sorted = quick_sort_Lomuto(cities)
    lomuto_time = time.time_ns() - start
    sorted_lists["lomuto"].append(lomuto_sorted)

    #quick sort hoare time
    start = time.time_ns()
    hoare_sorted = quick_sort_Hoare(cities)
    hoare_time = time.time_ns() - start
    sorted_lists["hoare"].append(hoare_sorted)

    #Write to files
    for algo, fname in sorted_files.items():
        with open(fname, "w") as f:
            for city_list in sorted_lists[algo]:
                line = " ".join(f"{city[0]} {city[1]}" for city in city_list)
                f.write(line + "\n")

    #Write runtime to file
    with open("runtimes.txt", "w") as f:
        for times in runtime:
            f.write(f"{times['merge']} {times['lomuto']} {times['hoare']}\n")


    x = list(range(1, len(merge_sort) + 1))
    #simply plots times against each run of bubble and selection sort
    plt.plot(x, merge_time, label="Merge Sort")
    plt.plot(x, lomuto_time, label="Quick Sort Lomuto")
    plt.plot(x, hoare_time, label="Quick Sort Hoare")

    #not part of data, just naming
    plt.xlabel("City Index (Line Number)")
    plt.ylabel("Runtime (nanoseconds)")
    plt.title("Sorting Runtime")

    plt.legend()

    plt.savefig("runtime_plot.png")
    plt.show()