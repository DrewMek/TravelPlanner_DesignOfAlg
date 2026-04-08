import ast
import time
import matplotlib.pyplot as plt

#Oliver Conley, Drew Meketi, and Ty Madsen
# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

# Merge function for Merge Sort
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

# Quick Sort Lomuto
def quick_sort_Lomuto(arr, low, high):
    def qsort(arr, low, high):
        if low < high:
            p = partition(arr, low, high)
            qsort(arr, low, p - 1)
            qsort(arr, p + 1, high)
            
    # Partition function for Lomuto
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

# Quick Sort Hoare
def quick_sort_Hoare(arr, low, high):
    def qsort(arr, low, high):
        if low < high:
            p = partition(arr, low, high)
            qsort(arr, low, p)
            qsort(arr, p + 1, high)

    # Partition function for Hoare
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

# Budget
B = 5000
trip_numbers = []

#stored sorted data
sorted_lists = {"merge": [], "lomuto": [], "hoare": []}
runtime = []

with open("roundtrip_costs.txt", "r") as f:
    lines = f.readlines()

# Process each city
for line in lines:
    line = line.strip()
    if not line:
        continue
    city_list = ast.literal_eval(line)

    # Measure Merge Sort
    start = time.time_ns()
    merge_sorted = merge_sort(city_list.copy())
    merge_time = time.time_ns() - start
    sorted_lists["merge"].append(merge_sorted)

    # Measure Lomuto
    start = time.time_ns()
    lomuto_sorted = quick_sort_Lomuto(city_list.copy(), 0, len(city_list)-1)
    lomuto_time = time.time_ns() - start
    sorted_lists["lomuto"].append(lomuto_sorted)

    # Measure Hoare
    start = time.time_ns()
    hoare_sorted = quick_sort_Hoare(city_list.copy(), 0, len(city_list)-1)
    hoare_time = time.time_ns() - start
    sorted_lists["hoare"].append(hoare_sorted)

    # Append runtime
    runtime.append((merge_time, lomuto_time, hoare_time))

    # Count trips under budget (use merge-sorted)
    total = 0
    count = 0
    for city, cost in merge_sorted:
        if total + cost <= B:
            total += cost
            count += 1
        else:
            break
    trip_numbers.append(count)

# Write sorted files
with open("merge_output.txt", "w") as f:
    for city_list in sorted_lists["merge"]:
        f.write(" ".join(f"{city} {cost}" for city, cost in city_list) + "\n")

with open("lomuto_output.txt", "w") as f:
    for city_list in sorted_lists["lomuto"]:
        f.write(" ".join(f"{city} {cost}" for city, cost in city_list) + "\n")

with open("hoare_output.txt", "w") as f:
    for city_list in sorted_lists["hoare"]:
        f.write(" ".join(f"{city} {cost}" for city, cost in city_list) + "\n")

# Write trip numbers
with open("trip_nums.txt", "w") as f:
    for num in trip_numbers:
        f.write(str(num) + "\n")

# Write runtime
with open("PA_2_runtime.txt", "w") as f:
    for mer, lom, hoa in runtime:
        f.write(f"({mer}, {lom}, {hoa})\n")


x = list(range(1, len(runtime) + 1))

merge_times = [r[0] for r in runtime] #these just grab the times from each individual method so we can plot them properly
lomuto_times = [r[1] for r in runtime]
hoare_times = [r[2] for r in runtime]

plt.figure(figsize=(10, 6)) #makes a figure
plt.plot(x, merge_times, marker='o', label="Merge Sort") #plots based on whats in the list
plt.plot(x, lomuto_times, marker='s', label="Quick Sort Lomuto")
plt.plot(x, hoare_times, marker='^', label="Quick Sort Hoare")

plt.xlabel("City Index (Line Number)") #labeling the plot and organizing it
plt.ylabel("Runtime (nanoseconds)")
plt.title("Sorting Runtime by City List")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("PA_2_runtime_plot.png")
plt.show()

#its kinda ugly so ill make it a bar chart
avg_merge = sum(merge_times) / len(merge_times)
avg_lomuto = sum(lomuto_times) / len(lomuto_times)
avg_hoare = sum(hoare_times) / len(hoare_times)

algorithms = ["Merge Sort", "Quick Sort Lomuto", "Quick Sort Hoare"]
averages = [avg_merge, avg_lomuto, avg_hoare]

plt.figure(figsize=(8, 5))
plt.bar(algorithms, averages)

plt.xlabel("Algorithm")
plt.ylabel("Average Runtime (nanoseconds)")
plt.title("Average Sorting Runtime")
plt.tight_layout()
plt.savefig("PA_2_avg_runtime_bar.png")
plt.show()
#way cleaner bar chart.  curious how hoare is slower, though.  is the implementation correct?