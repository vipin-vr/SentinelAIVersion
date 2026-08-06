const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");
const predictBtn = document.getElementById("predictBtn");
const result = document.getElementById("result");

// Railway Backend URL
const API_URL = "https://sentinelaiversion-production.up.railway.app/predict";

// Preview Image
imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (file) {
        previewImage.src = URL.createObjectURL(file);
    }

});

// Predict
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

        // -----------------------------
        // Invalid Image
        // -----------------------------
        if (data.isRoad === false) {

            outputImage.src = "";

            result.innerHTML = `
                <div style="
                    background:#ffebee;
                    color:#b71c1c;
                    padding:20px;
                    border-radius:12px;
                    border:2px solid red;
                    margin-top:20px;
                    text-align:center;
                ">
                    <h2>❌ Invalid Image</h2>

                    <p>Please upload a road or public infrastructure image.</p>

                    <h3>Supported Images</h3>

                    <ul style="list-style:none;padding:0;">
                        <li>✅ Road</li>
                        <li>✅ Highway</li>
                        <li>✅ Street</li>
                        <li>✅ Bridge</li>
                        <li>✅ Public Infrastructure</li>
                    </ul>
                </div>
            `;

            return;
        }

        // -----------------------------
        // Valid Prediction
        // -----------------------------
        outputImage.src = data.output_image + "?t=" + Date.now();

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