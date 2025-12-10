# FDA FAST OCLC and LCSH API Connectivity

**Repository:** [https://github.com/shravanxd/library_fda_api_test.git](https://github.com/shravanxd/library_fda_api_test.git)

## 1. Project Overview

This project contains Python scripts designed to establish and demonstrate connectivity with the OCLC FAST (Faceted Application of Subject Terminology) API and the Library of Congress Subject Headings (LCSH) API.

The primary goal is to confirm that the local environment can successfully reach these external services using standard HTTP requests. This validation ensures that downstream applications can reliably fetch authority records and subject suggestions.

The project consists of two main scripts:
*   `fast_api_test.py`: A diagnostic tool to verify working connectivity to FAST endpoints.
*   `fast_batch_search.py`: A bulk assessment tool that generates a comprehensive spreadsheet comparing LCSH and FAST matches side-by-side.

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

This script generates a **Complete Assessment Spreadsheet** for a list of terms. It queries both the Library of Congress (LCSH) and FAST APIs and pivots the results into a single row per term.

**Key Features:**
*   **Side-by-Side Comparison**: FAST and LCSH matches are aligned in a single row.
*   **LCSH Focus**: Prioritizes LCSH data, including Authoritative Labels and URIs for verification.
*   **Wide Format**: Optimized for supervisor assessment in spreadsheet software.

**How to Run:**
```bash
python3 fast_batch_search.py
```

**Output:**
*   Console preview of the assessment data.
*   `assessment_results.csv`: The complete dataset ready for review.

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

### 5.2. Assessment Spreadsheet Generation

Running `fast_batch_search.py` produces the `assessment_results.csv` file. Below is a preview of the pivoted data structure, designed for thorough value assessment:

```text
Generating Assessment Spreadsheet for 20 terms...

--- Assessment Spreadsheet Preview ---
      Search Term         LCSH_Label_1           LCSH_URI_1        FAST_Label_1
0           abuse             Abuse of  http://id.loc.go...               Abuse
1       education            Education  http://id.loc.go...           Education
2     immigration  Immigration advo...  http://id.loc.go...         Immigration
3          gender               Gender  http://id.loc.go...              Gender
4  climate change  Climate change a...  http://id.loc.go...  Changes in climate

Complete assessment spreadsheet exported to 'assessment_results.csv'
```

**Analysis:**
*   **Thorough Assessment**: The output organizes 20 terms into a clear, assessable format.
*   **LCSH Matching**: The `LCSH_Label_1` and `LCSH_URI_1` columns provide the specific authority data needed for validation.
*   **Assessment Ready**: The "wide" format allows for immediate comparison between the input term, the primary LCSH match, and the corresponding FAST term without needing to cross-reference multiple rows.

## 6. Conclusion

The execution of these scripts confirms that the environment is correctly configured to interact with external bibliographic APIs. Both `fast.oclc.org` and `id.loc.gov` are accessible, allowing for the seamless retrieval of subject headings and authority data.
