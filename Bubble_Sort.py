import re

# Process flights.txt
print("Flights:")

try:
    with open('flights.txt', 'r') as file:
        for line in file:
            flights = re.findall(r'\([^()]*\)', line)
            for flight in flights:
                print(flight)
except FileNotFoundError:
    print("Error: flights.txt not found.")

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
output_filename = "FtimeBubSort.txt"

with open(output_filename, 'w') as f:
    f.write("This is the first line.\n")
    f.write("This is the second line.\n")