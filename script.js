document.getElementById("downloadVideo").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const urlInput = document.getElementById("link").value; // Get the input value
    const responseElement = document.createElement("div"); // Create a div to display the response
    console.log("Video URL: ", urlInput);

    try {
        const response = await fetch("http://127.0.0.1:8002/download", { // Update the URL based on your FastAPI server
            method: "POST",
            headers: {
                "Content-Type": "text/plain" // Update content type to indicate a plain string
            },
            body: urlInput // Send the input value as a plain string
        });


        const data = await response.json(); // Parse the JSON response

        if (response.ok) {
            // If the response is successful
            responseElement.textContent = data.message + " Filename: " + data.filename;
            responseElement.style.color = "green";
        } else {
            // If there's an error
            responseElement.textContent = "Error: " + data.detail;
            responseElement.style.color = "red";
        }
    } catch (error) {
        // Handle any other errors
        responseElement.textContent = "An error occurred: " + error.message;
        responseElement.style.color = "red";
    }

    document.body.appendChild(responseElement); // Append the response message to the body
});
