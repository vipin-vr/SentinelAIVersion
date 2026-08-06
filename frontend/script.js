const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");
const predictBtn = document.getElementById("predictBtn");
const result = document.getElementById("result");

// Railway Backend URL
const API_URL = "https://sentinelaiversion-production.up.railway.app/predict";

// Preview selected image
imageInput.addEventListener("change", function () {

    const file = this.files[0];

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

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Prediction failed");
        }

        const data = await response.json();

        console.log(data);

        // Display output image
        outputImage.src = data.output_image + "?t=" + Date.now();

        // Display detection results
        let html = "";

        html += "<h2>Detection Result</h2>";
        html += "<h3>Total Objects : " + data.total_detections + "</h3>";
        html += "<ul>";

        data.detections.forEach(item => {
            html += `<li>${item.class} : ${item.confidence}</li>`;
        });

        html += "</ul>";

        result.innerHTML = html;

    }
    catch (err) {

        console.error(err);

        alert("Unable to connect to Sentinel AI Backend.");

    }

});