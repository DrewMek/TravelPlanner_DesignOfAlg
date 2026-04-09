#Oliver Conley, Drew Meketi, and Ty Madsen
import math
import time
import matplotlib.pyplot as plt

# Distance function
def distance(p1, p2):
    return math.sqrt((p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

# Brute Force
def brute_force(points):
    min_dist = float('inf')
    best_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                best_pair = (points[i], points[j])

    return best_pair, min_dist

# Divide & Conquer
def closest_rec(points):
    n = len(points)

    if n <= 3:
        return brute_force(points)

    mid = n // 2
    mid_x = points[mid][1]

    left_pair, left_dist = closest_rec(points[:mid])
    right_pair, right_dist = closest_rec(points[mid:])

    if left_dist < right_dist:
        d = left_dist
        best_pair = left_pair
    else:
        d = right_dist
        best_pair = right_pair

    strip = [p for p in points if abs(p[1] - mid_x) < d]
    strip.sort(key=lambda x: x[2])

    for i in range(len(strip)):
        for j in range(i+1, min(i+7, len(strip))):
            dist = distance(strip[i], strip[j])
            if dist < d:
                d = dist
                best_pair = (strip[i], strip[j])

    return best_pair, d

# MAIN
def main():

    # Read file
    cities = []
    with open("cities.txt") as f:
        for line in f:
            cid, x, y = line.split()
            cities.append((int(cid), float(x), float(y)))

    bf_file = open("BF-Closest.txt", "w")
    dc_file = open("DC-Closest.txt", "w")
    time_file = open("PA_3_runtimes.txt", "w")

    bf_times = []
    dc_times = []

    for i in range(50, 101):

        subset = cities[:i]

        # Brute Force time
        start = time.perf_counter_ns()
        pair_bf, dist_bf = brute_force(subset)
        bf_time = time.perf_counter_ns() - start

        # Divide & Conquer time
        subset_sorted = sorted(subset, key=lambda x: x[1])

        start = time.perf_counter_ns()
        pair_dc, dist_dc = closest_rec(subset_sorted)
        dc_time = time.perf_counter_ns() - start


        # Write outputs
        bf_file.write(f"{pair_bf[0][0]}, {pair_bf[1][0]}, {dist_bf}\n")
        dc_file.write(f"{pair_dc[0][0]}, {pair_dc[1][0]}, {dist_dc}\n")
        time_file.write(f"{bf_time}, {dc_time}\n")

        bf_times.append(bf_time)
        dc_times.append(dc_time)

        print(f"Finished i = {i}")

    bf_file.close()
    dc_file.close()
    time_file.close()

    # extra credit: plot runtimes
    plt.figure()

    
    plt.show()


main()