import requests
import json
import xml.dom.minidom

def fast_search(term):
    """
    Searches the FAST API using the verified working endpoint at fast.oclc.org.
    This bypasses the experimental.worldcat.org server which is unreachable.
    """
    print(f"Searching for term: '{term}' via fast.oclc.org...")
    
    # Verified working endpoint
    url = "https://fast.oclc.org/searchfast/fastsuggest"
    
    # 'suggestall' is the default field for general queries in this API
    params = {
        "query": term,
        "max": 10,
        "wt": "json"  # specific to Solr-based endpoints like this one
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        print("Search successful!")
        return r.json()
    except Exception as e:
        print(f"Search failed: {e}")
        return None

def fast_lookup(identifier):
    """
    Looks up a specific FAST record by ID.
    Uses 'application/rdf+xml' to avoid 406 Not Acceptable errors.
    """
    print(f"Looking up record ID: {identifier}...")
    url = f"https://id.worldcat.org/fast/{identifier}"
    
    # 'application/ld+json' fails with 406 on some networks/endpoints, so we use RDF/XML
    headers = {"Accept": "application/rdf+xml"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        print("Lookup successful!")
        return r.text
    except Exception as e:
        print(f"Lookup failed: {e}")
        return None

if __name__ == "__main__":
    print("=== FAST API Connectivity Test (Fixed) ===\n")

    # 1. Test Search
    print("--- 1. Testing Search (via fast.oclc.org) ---")
    search_results = fast_search("abuse")
    if search_results:
        # The response structure from this endpoint is typically Solr-like
        # {"response": {"docs": [...]}}
        print("Response Snippet:")
        print(json.dumps(search_results, indent=2)[:500] + "\n... (truncated)")
    
    print("\n" + "-"*30 + "\n")

    # 2. Test Record Lookup
    print("--- 2. Testing Record Lookup (via id.worldcat.org) ---")
    record_data = fast_lookup("802159")
    if record_data:
        print("Response Snippet (XML):")
        print(record_data[:300] + "\n... (truncated)")
    
    print("\n=== Test Complete ===")
