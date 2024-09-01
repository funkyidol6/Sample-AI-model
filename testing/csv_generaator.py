import csv
import random

# Set the number of rows and seeds
num_rows = 5000
num_seeds = 50

# Initialize CSV data
csv_data = []

# Generate CSV data
for seed in range(1, num_seeds + 1):
    random.seed(seed)
    last_value = 0

    for row in range(1, num_rows + 1):
        r_num = random.randint(1, 100)
        csv_data.append([seed, last_value, r_num])
        last_value = r_num

# Write CSV file
csv_filename = 'generated_data.csv'
header = ['Seed', 'Last', 'r_num']

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)
    csv_writer.writerows(csv_data)

print(f"CSV file '{csv_filename}' generated successfully.")
