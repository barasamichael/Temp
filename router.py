import csv

# Input and output file paths
input_file_path = 'routes.txt'
output_file_path = 'output.csv'

# Read the text file and split it into lines
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Remove unnecessary lines and headers
lines = [line.strip() for line in lines if line.strip() and not line.startswith('-')]

# Parse the lines and create a list of dictionaries
data = []
for line in lines:
    parts = line.split()
    if len(parts) == 3:
        endpoint = parts[0]
        methods = parts[1]
        rule = parts[2]
        data.append({'Endpoint': endpoint, 'Methods': methods, 'Rule': rule})

# Write the data to a CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    fieldnames = ['Endpoint', 'Methods', 'Rule']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    for row in data:
        writer.writerow(row)

print(f'Conversion completed. CSV file saved to {output_file_path}')
