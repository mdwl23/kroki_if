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

// Function to change the content of the text area based on the selected diagram type
function changeTextArea(diagramType) {
    var textArea = document.getElementById("text_data");
    if (diagramType === "graphviz") {
        // Set Graphviz code in the text area
        textArea.value = 'digraph G {\n  graph [fontname = "Meiryo UI"];\n  node [fontname = "Meiryo UI"];\n  edge [fontname = "Meiryo UI"];\n  Hello->World\n}';
    } else if (diagramType === "mermaid") {
        // Set Mermaid code in the text area
        textArea.value = 'graph TD\n  A[Hello] -->|World| B[World]';
    } else if (diagramType === "plantuml") {
        // Set PlantUML code in the text area
        textArea.value = 'skinparam defaultFontName Meiryo\n\nrectangle "hello" as hello\nrectangle "world" as world\nhello-->world';
    }
}
