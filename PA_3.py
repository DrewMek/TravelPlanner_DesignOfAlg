#Oliver Conley, Drew Meketi, and Ty Madsen
import time
import matplotlib.pyplot as plt

# Distance function to calculate the distance between two points
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

#brute force algorithm to find the closest pair of points
def brute_force(points):
    
    min_dist = float('inf')
    
    closest_pair = None
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    
    return closest_pair, min_dist

#Divide and conquer algorithm to find the closest pair of points
def closest_pair(points):
   
    if len(points) <= 3:
        return brute_force(points)
    
    mid = len(points) // 2 
    left_half = points[:mid] 
    right_half = points[mid:]

    (p1, q1), left_dist = closest_pair(left_half) 
    (p2, q2), right_dist = closest_pair(right_half)

    if left_dist < right_dist:
        min_dist = left_dist
        closest_pair = (p1, q1)
    else:
        min_dist = right_dist
        closest_pair = (p2, q2)

    mid_x = points[mid][0]
    
    # Create a strip of points within min_dist of the midline
    strip = [point for point in points if abs(point[0] - mid_x) < min_dist]
    strip.sort(key=lambda point: point[1])

    # Check the strip for closer pairs
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (strip[i], strip[j])

    return closest_pair, min_dist

def main():
    #read cities file
    cities = []
    with open('cities.txt', 'r') as file:
        for line in file:
            name, x, y = line.strip().split()
            cities.append((name, float(x), float(y)))

    # Sort cities by x-coordinate
    cities.sort(key=lambda city: city[1])

    # Find the closest pair of cities
    closest_pair, min_dist = closest_pair(cities)

    print(f"Closest pair: {closest_pair[0][0]} and {closest_pair[1][0]}")
    print(f"Distance: {min_dist}")

    #output files
    bf_file = open("BF-Closest.txt", "w")
    dc_file = open("DC-Closest.txt", "w")
    time_file = open("runtime.txt", "w")

    for i in range(50, 101):
        
        #brute force time
        start_time = time.time()
        brute_force(cities[:i])
        bf_time = time.time() - start_time

        #divide and conquer time
        start_time = time.time()
        closest_pair(cities[:i])
        dc_time = time.time() - start_time

        #write times to file
        bf_file.write(f"{i} {bf_time}\n")
        dc_file.write(f"{i} {dc_time}\n")
        time_file.write(f"{i} {bf_time} {dc_time}\n")

    #close files
    bf_file.close()
    dc_file.close()
    time_file.close()

    #plotting the results on a graph
    


if __name__ == "__main__":
    main()