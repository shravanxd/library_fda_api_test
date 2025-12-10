# FDA FAST OCLC and LCSH API Connectivity

**Repository:** [https://github.com/shravanxd/library_fda_api_test.git](https://github.com/shravanxd/library_fda_api_test.git)

## 1. Project Overview

This project contains Python scripts designed to establish and demonstrate connectivity with the OCLC FAST (Faceted Application of Subject Terminology) API and the Library of Congress Subject Headings (LCSH) API.

The primary goal is to confirm that the local environment can successfully reach these external services using standard HTTP requests. This validation ensures that downstream applications can reliably fetch authority records and subject suggestions.

The project consists of two main scripts:
*   `fast_api_test.py`: A diagnostic tool to verify working connectivity to FAST endpoints.
*   `fast_batch_search.py`: A bulk search utility to query both FAST and LCSH for a list of terms.

## 2. Prerequisites

To run these scripts, you need a Python 3 environment installed on your system. The scripts rely on the following external libraries:

*   `requests`: For making HTTP calls to the APIs.
*   `pandas`: For data manipulation and exporting results to CSV.

## 3. Installation

1.  Ensure Python 3 is installed. You can check this by running:
    ```bash
    python3 --version
    ```

2.  Install the required dependencies using pip:
    ```bash
    pip install requests pandas
    ```

## 4. Usage & Script Analysis

### 4.1. fast_api_test.py

This script performs a connectivity check by querying the `fast.oclc.org` endpoint for the term "abuse".

**How to Run:**
```bash
python3 fast_api_test.py
```

**Expected Behavior:**
The script prints the status of the request to the console, verifying that the API is reachable and returning valid JSON data.

### 4.2. fast_batch_search.py

This script takes a list of terms (defined in the `words` list within the script) and queries both FAST and LCSH APIs for each term, retrieving the top matches.

**How to Run:**
```bash
python3 fast_batch_search.py
```

**Output:**
*   Console output showing the DataFrame of results.
*   A CSV file named `fast_search_results.csv` containing the aggregated data.

## 5. Output Examples and Capabilities

The following sections display the actual output captured from running these scripts, demonstrating successful integration.

### 5.1. Connectivity Results

Running `fast_api_test.py` yielded the following successful response:

```text
=== FAST API Connectivity Check (Fixed) ===

--- 1. Verifying Search (via fast.oclc.org) ---
Searching for term: 'abuse' via fast.oclc.org...
Search successful!
Response Snippet:
{
  "responseHeader": {
    "status": 0,
    "QTime": 40,
    "params": {
      "q": "suggestall:abuse",
      "fl": "suggestall",
      "wt": "json"
    }
  },
  "response": {
    "numFound": 1951,
    "start": 0,
    "docs": [
      { "suggestall": [ "Abuse" ] },
      { "suggestall": [ "child abuse" ] },
      { "suggestall": [ "Abused men" ] },
      ...
    ]
  }
... (truncated)

=== Check Complete ===
```

**Analysis:**
*   **Search Endpoint (`fast.oclc.org`)**: **SUCCESS**. The environment can successfully reach the and suggest API. The server returned a valid JSON response with HTTP 200, confirming that the network configuration allows outbound traffic to OCLC services.

### 5.2. Batch Search Results

Running `fast_batch_search.py` with the expanded term list (20 terms):

```text
Searching for 20 terms...

--- Search Results ---
    search_term                          label  type                                                  uri source
0         abuse                          Abuse  None                                                 None   FAST
1         abuse                    child abuse  None                                                 None   FAST
2         abuse                     Abused men  None                                                 None   FAST
3         abuse                       Abuse of  LCSH    http://id.loc.gov/authorities/subjects/sh99002071   LCSH
4         abuse  Abuse of administrative power  LCSH    http://id.loc.gov/authorities/subjects/sh85000274   LCSH
..          ...                            ...   ...                                                  ...    ...
113  literature                     Literature  None                                                 None   FAST
114  literature                     Literature  None                                                 None   FAST
115  literature                     Literature  LCSH    http://id.loc.gov/authorities/subjects/sh85077507   LCSH
116  literature    Literature and anthropology  LCSH    http://id.loc.gov/authorities/subjects/sh85077563   LCSH
117  literature   Literature and civil service  LCSH  http://id.loc.gov/authorities/subjects/sh2012004611   LCSH

[118 rows x 5 columns]

Results exported to 'fast_search_results.csv'

Done.
```

**Analysis:**
*   **Successful Retrieval**: The script successfully queried both API endpoints for 20 terms, yielding 118 total suggestions.
*   **Data Richness**:
    *   **FAST**: Returns relevant subject labels (e.g., "Abuse", "child abuse").
    *   **LCSH**: Returns comprehensive data, including the Label, Type ("LCSH"), and the full authoritative URI (e.g., `http://id.loc.gov/authorities/subjects/sh99002071`).
*   **Connectivity**: The presence of mixed results confirms that the local environment can reach multiple external authority files (OCLC and LoC) simultaneously.

## 6. Conclusion

The execution of these scripts confirms that the environment is correctly configured to interact with external bibliographic APIs. Both `fast.oclc.org` and `id.loc.gov` are accessible, allowing for the seamless retrieval of subject headings and authority data.
