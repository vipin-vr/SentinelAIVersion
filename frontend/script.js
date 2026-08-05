const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");
const predictBtn = document.getElementById("predictBtn");
const result = document.getElementById("result");

// Preview selected image
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if (file) {
        previewImage.src = URL.createObjectURL(file);
    }
});

// Predict button
predictBtn.addEventListener("click", async () => {

    if (imageInput.files.length === 0) {
        alert("Please select an image.");
        return;
    }

    const formData = new FormData();
    formData.append("file", imageInput.files[0]);

    result.innerHTML = "<h3>Predicting...</h3>";
    outputImage.src = "";

    try {

        const response = await fetch(
            "https://sentinelai-a6aj.onrender.com/predict",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Server Error: " + response.status);
        }

        const data = await response.json();

        console.log(data);

        // Show detected image
        outputImage.src = data.output_image + "?t=" + Date.now();

        // Show detection results
        let html = `
            <h2>Detection Result</h2>
            <h3>Total Objects : ${data.total_detections}</h3>
            <ul>
        `;

        data.detections.forEach(item => {
            html += `<li>${item.class} : ${item.confidence}</li>`;
        });

        html += "</ul>";

        result.innerHTML = html;

    } catch (error) {

        console.error("Fetch Error:", error);

        alert("Unable to connect to FastAPI Backend");

        result.innerHTML = `
            <h3 style="color:red;">
                Failed to connect to backend.
            </h3>
        `;
    }

});