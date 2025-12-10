import requests
import pandas as pd

FAST_SEARCH_URL = "https://fast.oclc.org/searchfast/fastsuggest"
LCSH_SEARCH_URL = "https://id.loc.gov/authorities/subjects/suggest"

def fast_top3(term):
    """Return top 3 FAST matches for a search term."""
    # fast.oclc.org only supports 'suggestall' field in this endpoint
    # fast.oclc.org only supports 'suggestall' field in this endpoint
    params = {"query": term, "max": 3, "wt": "json"}
    try:
        r = requests.get(FAST_SEARCH_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        # The fast.oclc.org 'fastsuggest' endpoint returns docs with only 'suggestall' (list of strings)
        # It does NOT return IDs, 'type', or 'label' fields like the standard AssignFAST API.
        docs = data.get("response", {}).get("docs", [])
        results = []

        for d in docs[:3]:
            # extract the first suggestion string
            label = d.get("suggestall", ["Unknown"])[0] if d.get("suggestall") else None
            
            results.append({
                "search_term": term,
                "fast_id": None, # ID not available from this endpoint
                "label": label,
                "type": None,    # Type not available
                "uri": None      # URI needs ID
            })

        return results
    except Exception as e:
        print(f"Error searching FAST for '{term}': {e}")
        return []

def lcsh_search(term):
    """Return top 3 LCSH matches from Library of Congress."""
    params = {"q": term} # OpenSearch suggest parameter
    try:
        r = requests.get(LCSH_SEARCH_URL, params=params, timeout=10)
        r.raise_for_status()
        # Response is OpenSearch format: [query, [labels], [descriptions], [uris]]
        # e.g. ["abuse", ["Abuse of", ...], ["1 result", ...], ["http://...", ...]]
        data = r.json()
        
        if not data or len(data) < 4:
            return []
            
        labels = data[1]
        uris = data[3]
        
        results = []
        # Get top 3 or fewer
        count = min(len(labels), 3)
        
        for i in range(count):
            results.append({
                "search_term": term,
                "fast_id": None, # Not applicable
                "label": labels[i],
                "type": "LCSH",
                "uri": uris[i]
            })
            
        return results
    except Exception as e:
        print(f"Error searching LCSH for '{term}': {e}")
        return []


if __name__ == "__main__":
    # Test multiple words (20 terms)
    words = [
        "abuse", "education", "immigration", "gender", "climate change",
        "artificial intelligence", "democracy", "mental health", "sustainability", "human rights",
        "globalization", "poverty", "racism", "social media", "pandemic",
        "epidemiology", "genetics", "philosophy", "history", "literature"
    ]

    print(f"Generating Assessment Spreadsheet for {len(words)} terms...")
    
    assessment_data = []

    for w in words:
        row = {"Search Term": w}
        
        # --- LCSH Results (Priority) ---
        lcsh_res = lcsh_search(w)
        # Add top 3 LCSH matches to the row
        for i in range(3):
            suffix = f"_{i+1}"
            if i < len(lcsh_res):
                row[f"LCSH_Label{suffix}"] = lcsh_res[i].get("label")
                row[f"LCSH_URI{suffix}"] = lcsh_res[i].get("uri")
            else:
                row[f"LCSH_Label{suffix}"] = None
                row[f"LCSH_URI{suffix}"] = None

        # --- FAST Results ---
        fast_res = fast_top3(w)
        # Add top 3 FAST matches to the row
        for i in range(3):
            suffix = f"_{i+1}"
            if i < len(fast_res):
                row[f"FAST_Label{suffix}"] = fast_res[i].get("label")
                # FAST suggest endpoint doesn't give URIs/IDs cleanly, so just Label
            else:
                row[f"FAST_Label{suffix}"] = None

        assessment_data.append(row)

    # Create DataFrame
    df = pd.DataFrame(assessment_data)
    
    # improved display settings for terminal
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 20)
    
    print("\n--- Assessment Spreadsheet Preview ---")
    print(df[["Search Term", "LCSH_Label_1", "LCSH_URI_1", "FAST_Label_1"]].head())
    
    # Export to CSV
    csv_filename = "assessment_results.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nComplete assessment spreadsheet exported to '{csv_filename}'")
    
    print("\nDone.")
