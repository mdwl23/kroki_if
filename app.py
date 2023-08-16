from flask import Flask, request
import base64
import zlib
import requests

app = Flask(__name__)

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

@app.route("/")
def index():
    # Render HTML template with form and input tags
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>Dragon Generator</title>
    </head>
    <body>
        <h1>Dragon Generator</h1>
        <p>Graphvizのテキストデータを入力してください。</p>
        <form action="/" method="POST">
            <textarea name="text_data" rows="10" cols="50"></textarea>
            <input type="submit" value="送信">
        </form>
    </body>
    </html>
    """

@app.route("/", methods=["POST"])
def generate():
    # Get text data from form
    text_data = request.form["text_data"]
    # Create Kroki instance
    # kroki = Kroki(host="localhost", port=8000)
    kroki = Kroki(host="kroki", port=8000)
    # Call send_data method and get image binary data
    image_bytes = kroki.send_data(text_data)
    # Return image binary data as SVG format
    return image_bytes, 200, {"Content-Type": "image/svg+xml"}
