#!/usr/bin/env python3
import argparse
import json
import matplotlib.pyplot as plt

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true', help='Normalize values to percentages')
parser.add_argument('--output', default='bargraph.png', help='Output PNG filename')
args = parser.parse_args()

# Load JSON data from the input file
with open(args.input_path) as f:
    counts = json.load(f)

# Normalize the counts by the total values if --percent is given
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# Convert the dictionary to a list of (key, value) tuples
items = list(counts[args.key].items())

# Get the top 10 keys by value (highest values)...
top_items_desc = sorted(items, key=lambda x: x[1], reverse=True)[:10]
# ...then sort those top 10 items in ascending order (low to high)
top_items = sorted(top_items_desc, key=lambda x: x[1])

# Separate keys and values for plotting
keys = [item[0] for item in top_items]
values = [item[1] for item in top_items]

# Create the bar graph
plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.xlabel(args.key)
plt.ylabel('Percentage' if args.percent else 'Count')
plt.title(f"Top 10 {args.key} Values")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig(args.output)
print(f"Bar graph saved as {args.output}")

