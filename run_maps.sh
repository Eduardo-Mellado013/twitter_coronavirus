for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
    echo "Processing $file"
    nohup python3 src/map.py --input_path "$file" > "log_$(basename "$file").txt" 2>&1 &
done
echo "All processes started."
