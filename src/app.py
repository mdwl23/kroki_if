from flask import Flask, request
import base64
import zlib
import requests

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
    # Render HTML template with form, input, and img tags
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>Dragon Generator</title>
        <script>
            // Define a function to handle form submission
            function submitForm(event) {
                // Prevent default behavior of form submission
                event.preventDefault();
                
                // Create XMLHttpRequest object
                var xhr = new XMLHttpRequest();
                
                // Open POST request to root path asynchronously
                xhr.open("POST", "/", true);
                
                // Set request header for form data
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                
                // Define a function to handle response
                xhr.onreadystatechange = function() {
                    // Check if ready state is 4 (done) and status is 200 (OK)
                    if (xhr.readyState == 4 && xhr.status == 200) {
                        // Get image URL from response text
                        var imageUrl = xhr.responseText;
                        // Get image element by id
                        var image = document.getElementById("image");
                        // Set image source attribute to image URL
                        image.src = imageUrl;
                    }
                };
                
                // Get text data from form element by name
                var textData = document.forms[0].elements["text_data"].value;
                
                // Get selected diagram type
                var diagramType = document.querySelector('input[name="diagram_type"]:checked').value;
                
                // Encode text data with encodeURIComponent function
                var encodedTextData = encodeURIComponent(textData);
                
                // Send request with encoded text data and diagram type as parameters
                xhr.send("text_data=" + encodedTextData + "&diagram_type=" + diagramType);
            }
        </script>
    </head>
    <body>
        <h1>Dragon Generator</h1>
        <p>Graphvizのテキストデータを入力してください。</p>
            <form onsubmit="submitForm(event)">
                <textarea name="text_data" rows="10" cols="50">digraph G {\n  graph [fontname = "Meiryo UI"];\n  node [fontname = "Meiryo UI"];\n  edge [fontname = "Meiryo UI"];\n  Hello->World\n}</textarea>
                
                <p>Select diagram type:</p>
                <input type="radio" name="diagram_type" value="graphviz" checked> Graphviz
                <input type="radio" name="diagram_type" value="mermaid"> Mermaid
                
                <input type="submit" value="送信">
            </form>
        <img id="image" src="">
    </body>
    </html>
    """

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
