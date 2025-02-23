#!/usr/bin/env python3
import argparse
import json
import os
import glob
import datetime
import re
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict

# ---------------------------
# Set Up Font
# ---------------------------
# Use the system-installed Noto Sans font.
matplotlib.rcParams['font.family'] = 'Noto Sans'
print("Using font:", matplotlib.rcParams['font.family'])

# ---------------------------
# Argument Parsing
# ---------------------------
parser = argparse.ArgumentParser(
    description="Alternative Reduce: Plot daily tweet counts per hashtag using individual mapping output files."
)
parser.add_argument(
    '--hashtags', 
    nargs='+', 
    required=True,
    help='List of hashtags to plot (e.g., "#coronavirus" "#코로나바이러스")'
)
parser.add_argument(
    '--input_folder',
    default='outputs',
    help='Folder containing individual mapping output files (default: outputs)'
)
parser.add_argument(
    '--output',
    default='lineplot.png',
    help='Output PNG filename. (If not provided, a filename will be auto-generated from the hashtags)'
)
args = parser.parse_args()

# Auto-generate the output filename if the default is used.
if args.output == 'lineplot.png':
    sanitized = []
    for h in args.hashtags:
        h_clean = h.lstrip('#')              # remove the '#' character
        h_clean = re.sub(r'\W+', '_', h_clean)  # replace non-word characters with underscore
        sanitized.append(h_clean)
    args.output = '_'.join(sanitized) + "_lineplot.png"

# ---------------------------
# Data Aggregation from Individual Files
# ---------------------------
# We assume each mapping output file is named like "geoTwitter20-02-14.zip.lang".
# The date string is extracted from the filename and converted to the day-of-year.
hashtag_data = { hashtag: defaultdict(int) for hashtag in args.hashtags }

# Look for files with a .lang extension in the input folder.
file_pattern = os.path.join(args.input_folder, '*.lang')
file_list = glob.glob(file_pattern)

if not file_list:
    print("No mapping output files found in folder:", args.input_folder)
    exit(1)

for filepath in file_list:
    basename = os.path.basename(filepath)
    # Check if the filename follows the expected pattern.
    if not basename.startswith("geoTwitter") or ".zip" not in basename:
        continue

    try:
        # Extract the date portion from a filename like "geoTwitter20-02-14.zip.lang"
        core = basename[len("geoTwitter"):]  # e.g., "20-02-14.zip.lang"
        date_str = core.split(".zip")[0]       # e.g., "20-02-14"
        dt = datetime.datetime.strptime(date_str, "%y-%m-%d")
        day_of_year = dt.timetuple().tm_yday
    except Exception as e:
        print(f"Skipping file {basename}: could not parse date ({e})")
        continue

    try:
        with open(filepath, 'r') as f:
            mapping = json.load(f)
    except Exception as e:
        print(f"Error loading {basename}: {e}")
        continue

    # For each provided hashtag, sum the counts (across subcategories) for this day.
    for hashtag in args.hashtags:
        if hashtag in mapping:
            total = sum(mapping[hashtag].values())
        else:
            total = 0
        hashtag_data[hashtag][day_of_year] += total

# ---------------------------
# Determine Overall Day Range
# ---------------------------
all_days = set()
for hashtag in args.hashtags:
    all_days.update(hashtag_data[hashtag].keys())
if not all_days:
    print("No day information found in the mapping files for the given hashtags.")
    exit(1)
min_day = min(all_days)
max_day = max(all_days)
days = list(range(min_day, max_day + 1))

# ---------------------------
# Plotting
# ---------------------------
plt.figure(figsize=(12, 8))
for hashtag in args.hashtags:
    # Create a list of tweet counts for every day in the range (default to 0 if no data exists).
    counts_per_day = [hashtag_data[hashtag].get(day, 0) for day in days]
    plt.plot(days, counts_per_day, marker='o', label=hashtag)

plt.xlabel("Day of Year")
plt.ylabel("Number of Tweets")
plt.title("Daily Tweet Counts per Hashtag")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(args.output)
print(f"Line plot saved as {args.output}")

