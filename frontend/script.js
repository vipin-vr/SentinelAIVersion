const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");
const outputImageContainer = document.getElementById("outputImageContainer");
const predictBtn = document.getElementById("predictBtn");
const result = document.getElementById("result");
const previewContainer = document.getElementById("previewContainer");

// Preview selected image
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if (file) {
        previewContainer.style.display = "block";
        previewImage.src = URL.createObjectURL(file);
        outputImageContainer.style.display = "none";
        result.innerHTML = "";
    }
});

// Predict button
predictBtn.addEventListener("click", async () => {

    if (imageInput.files.length === 0) {
        alert("Please select an image.");
        return;
    }

    // Disable button and show loading state
    predictBtn.disabled = true;
    predictBtn.textContent = "Predicting...";

    const formData = new FormData();
    formData.append("file", imageInput.files[0]);

    result.innerHTML = "<h3>Predicting...</h3>";
    outputImage.src = "";

    try {

        const response = await fetch("https://sentinelai-a6aj.onrender.com/predict", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error: ${response.status} ${response.statusText}. ${errorText}`);
        }

        const data = await response.json();

        console.log(data);

        // Show detected image
        if (data.output_image) {
            outputImage.src = data.output_image + "?t=" + Date.now(); // Cache-busting
            outputImageContainer.style.display = "block";
        }

        // Show detection results
        if (data.detections) {
            const counts = {
                pothole: 0,
                crack: 0,
                manhole: 0,
            };

            data.detections.forEach(item => {
                if (item.class in counts) {
                    counts[item.class]++;
                }
            });

            let html = `
                <h2>Detection Result</h2>
                <p><strong>Total Issues Detected:</strong> ${data.total_detections}</p>
                <div class="counts">
                    <p><strong>Cracks:</strong> ${counts.crack}</p>
                    <p><strong>Potholes:</strong> ${counts.pothole}</p>
                    <p><strong>Manholes:</strong> ${counts.manhole}</p>
                </div>
            `;

            if (data.total_detections > 0) {
                html += '<h3>Details:</h3><ul>';
                data.detections.forEach(item => {
                    html += `<li>${item.class}: ${item.confidence.toFixed(2)}</li>`;
                });
                html += "</ul>";
            } else {
                html += "<p>No issues detected in the image.</p>";
            }
            result.innerHTML = html;
        }

    } catch (error) {

        console.error("Fetch Error:", error);

        result.innerHTML = `
            <h3 style="color:red;">
                An error occurred during prediction.
            </h3>
            <p style="color:red;">Please check the console for more details or try again. The backend server might be starting up.</p>
        `;

    } finally {
        // Re-enable button
        predictBtn.disabled = false;
        predictBtn.textContent = "Predict";
    }

});