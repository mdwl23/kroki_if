import sys
import base64
import zlib
import requests

class Kroki:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port

    def send_data(self, text_data):
        # Convert text data to bytes
        data_bytes = text_data.encode("utf-8")
        # Compress data bytes with zlib
        compressed_bytes = zlib.compress(data_bytes, 9)
        # Encode compressed bytes with base64
        encoded_bytes = base64.urlsafe_b64encode(compressed_bytes)
        # Convert encoded bytes to string
        encoded_string = encoded_bytes.decode("utf-8")
        # Create URL with server address, port, diagram library, and output format
        url = f"http://{self.host}:{self.port}/graphviz/svg/{encoded_string}"
        # Send GET request and get response object
        response = requests.get(url)
        # Check HTTP status code
        if response.status_code == 200:
            # Get image binary data from response content
            image_bytes = response.content
            # Return image binary data
            return image_bytes

if __name__ == "__main__":
    # Create Kroki instance
    kroki = Kroki()
    # Assign text data to variable
    text_data = "digraph G {\n  Hello->World\n}"
    # Call send_data method and get image binary data
    image_bytes = kroki.send_data(text_data)
    # Write image binary data to file
    with open("graph.svg", "wb") as f:
        f.write(image_bytes)

