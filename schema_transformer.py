import json
import re

def parse_authors(authorship_str):
    """
    Parses an authorship string into a list of Schema.org Person or Organization objects.
    Handles "et al." or ".." representation by keeping the explicit names.
    """
    authors_schema = []
    
    # Clean up the string
    authorship_str = authorship_str.replace("..,", "").replace("..", "").strip()
    
    # Check if it is a Consortium or Initiative (Organization)
    if any(x in authorship_str for x in ["Consortium", "Initiative", "Group", "Project"]):
        return [{
            "@type": "Organization",
            "name": authorship_str
        }]

    # Assume list of people (e.g., "Yu J, Hu S, Yang H")
    # Split by comma
    names = [n.strip() for n in authorship_str.split(',') if n.strip()]
    
    for name in names:
        parts = name.split(' ')
        person = {
            "@type": "Person",
            "name": name
        }
        
        # Heuristic: "Family Given" or "Given Family" detection
        # If name is "Yu J", Family=Yu, Given=J
        if len(parts) >= 2:
            person["familyName"] = parts[0]
            person["givenName"] = " ".join(parts[1:])
        else:
             person["familyName"] = name
             
        authors_schema.append(person)
        
    return authors_schema

def transform_genome_entry(entry):
    """Maps a single genome entry to Schema.org/Dataset."""
    
    # 1. Determine Scientific Name and Common Name
    # Some entries use 'Genus' and have a list of 'Species', others have 'ScientificName'
    sci_name = entry.get("ScientificName", entry.get("Genus", "Unknown Organism"))
    common_name = entry.get("common", "")
    
    # 2. Construct Description
    # specific description handling for entries with nested Species lists
    desc_parts = [f"Genomic dataset for {sci_name}."]
    if common_name:
        desc_parts.append(f"Commonly known as {common_name}.")
    
    if "GenomeSize" in entry:
        desc_parts.append(f"Genome size: {entry['GenomeSize']} Mb.")
    
    if "Species" in entry and isinstance(entry["Species"], list):
        species_list = [s.get("ScientificName") for s in entry["Species"] if "ScientificName" in s]
        desc_parts.append(f"Includes data for: {', '.join(species_list)}.")
        
    if "Source" in entry:
        desc_parts.append(f"Originally published in: {entry['Source']}")

    full_description = " ".join(desc_parts)

    # 3. Construct Keywords
    keywords = [sci_name, entry.get("className", ""), entry.get("group", ""), common_name]
    keywords_str = ", ".join([k for k in keywords if k])

    # 4. Build the Schema.org Object
    schema_obj = {
        "@context": "http://schema.org",
        "@type": "Dataset",
        "@id": f"https://doi.org/{entry.get('PubDoi', '')}", # Constructing a URI for ID
        "identifier": entry.get("PubDoi", ""),
        "name": entry.get("Title", f"Genome of {sci_name}"),
        "description": full_description,
        "datePublished": entry.get("start", entry.get("PubYear", "")),
        "keywords": keywords_str,
        "license": "https://creativecommons.org/licenses/by/4.0/", # Example license
        "citation": entry.get("Source", ""),
        "publisher": {
            "@type": "Organization",
            "name": "Forschungszentrum Juelich GmbH, IBG-4 Bioinformatics, Wilhelm-Johnen-Str., D-52428 Juelich, Germany" 
        }
    }

    # 5. Add Authors
    if "Authorship" in entry:
        authors_data = parse_authors(entry["Authorship"])
        schema_obj["author"] = authors_data
        schema_obj["creator"] = authors_data # Frequently synonymous in Dataset profile

    return schema_obj

def transform_json(input_json):
    """Main transformation loop."""
    output_data = []
    
    # Handle the specific structure of genomes_timeline1.json
    genome_list = input_json.get("genomes", [])
    
    for entry in genome_list:
        try:
            transformed = transform_genome_entry(entry)
            output_data.append(transformed)
        except Exception as e:
            print(f"Skipping entry due to error: {e}")
            continue
            
    return output_data

if __name__ == "__main__":
    # Local test execution
    try:
        with open('genomes_timeline1.json', 'r') as f:
            source_data = json.load(f)
        
        result = transform_json(source_data)
        
        with open('transformed_genomes.json', 'w') as f:
            json.dump(result, f, indent=2)
            
        print(f"Successfully transformed {len(result)} records.")
    except FileNotFoundError:
        print("File genomes_timeline1.json not found for local test.")