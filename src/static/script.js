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
