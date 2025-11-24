import json
import urllib.request
import os
# Import your existing transformation logic
from schema_transformer import transform_json

# Configuration
DATA_URL = "https://www.plabipd.de/json/genomes_timeline1.json"
OUTPUT_DIR = "public"
OUTPUT_FILENAME = "genomes.json"

def build_static_api():
    # 1. Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 2. Fetch Data
    print(f"Fetching data from {DATA_URL}...")
    req = urllib.request.Request(
        DATA_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (GenomeTransformer/1.0)'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise Exception(f"HTTP Error: {response.status}")
                
            content = response.read().decode('utf-8')
            raw_data = json.loads(content)
            
            # 3. Transform Data
            transformed_data = transform_json(raw_data)
            print(f"Transformed {len(transformed_data)} records.")

            # 4. Save to Disk (This is what GitHub Pages will host)
            output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(transformed_data, f, indent=2)
            
            print(f"Success! Static API generated at: {output_path}")

    except Exception as e:
        print(f"Build failed: {e}")
        exit(1)

if __name__ == "__main__":
    build_static_api()