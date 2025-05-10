import http.client  # Imports the 'http.client' module, providing tools for making HTTP and HTTPS requests.
import json  # Imports the 'json' module, used for working with JSON (JavaScript Object Notation) data.

conn = http.client.HTTPSConnection("api.lloydsbank.com")  # Creates an HTTPS connection object to the specified Lloyds Bank API server.
headers = {  # Defines a dictionary to store HTTP request headers.
    'If-Modified-Since': "REPLACE_THIS_VALUE",  # Header to request the resource only if it has been modified since the specified date (placeholder).
    'If-None-Match': "REPLACE_THIS_VALUE",  # Header to request the resource only if its entity tag (ETag) doesn't match the specified tag (placeholder).
    'accept': "application/prs.openbanking.opendata.v2.2+json"  # Header specifying the preferred media type for the response data (JSON in this specific Open Banking format).
}
conn.request("GET", "/open-banking/v2.2/branches", headers=headers)  # Sends an HTTP GET request to the '/open-banking/v2.2/branches' endpoint on the connected server, including the defined headers.
res = conn.getresponse()  # Retrieves the HTTP response object from the server.

if res.status == 200:  # Checks if the HTTP status code of the response is 200, indicating a successful request.
    data = res.read().decode("utf-8")  # Reads the response body (which is in bytes) and decodes it into a string using UTF-8 encoding.
    with open('branches.json', 'w') as f:  # Opens a file named 'branches.json' in write mode ('w'). The 'with' statement ensures the file is automatically closed.
        json.dump(json.loads(data), f, indent=4)  # Parses the JSON string ('data') into a Python object and then writes it to the file 'f' in a human-readable format with an indentation of 4 spaces.
    print("Data saved to branches.json")  # Prints a confirmation message to the console.
else:  # If the HTTP status code indicates an error.
    print(f"Error: {res.status} {res.reason}")  # Prints an error message to the console, including the HTTP status code and the reason for the error provided by the server.
