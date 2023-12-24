from flask import Flask, render_template, request, jsonify
import base64
import zlib

app = Flask(__name__)

class Kroki:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port

    def send_data(self, text_data, diagram_library="graphviz"):
        # Convert text data to bytes
        data_bytes = text_data.encode("utf-8")
        # Compress data bytes with zlib
        compressed_bytes = zlib.compress(data_bytes, 9)
        # Encode compressed bytes with base64
        encoded_bytes = base64.urlsafe_b64encode(compressed_bytes)
        # Convert encoded bytes to string
        encoded_string = encoded_bytes.decode("utf-8")

        # Create URL with server address, port, diagram library, and output format
        url = f"http://{self.host}:{self.port}/{diagram_library}/svg/{encoded_string}"

        # Return URL as string
        return url

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generate():
    # Get text data and diagram type from form
    text_data = request.form["text_data"]
    diagram_type = request.form["diagram_type"]

    # Create Kroki instance
    kroki = Kroki(host="localhost", port=8000)

    # Determine the diagram library and call the appropriate method
    if diagram_type == "graphviz":
        image_url = kroki.send_data(text_data, diagram_library="graphviz")
    elif diagram_type == "mermaid":
        image_url = kroki.send_data(text_data, diagram_library="mermaid")
    else:
        # Handle invalid diagram type
        return jsonify({"error": "Invalid diagram type"}), 400

    # Return image URL as plain text
    return image_url, 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(debug=True)
