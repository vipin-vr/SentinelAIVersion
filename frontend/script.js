const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");
const predictBtn = document.getElementById("predictBtn");
const result = document.getElementById("result");

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if(file){

        previewImage.src = URL.createObjectURL(file);

    }

});

predictBtn.addEventListener("click", async ()=>{

    if(imageInput.files.length===0){

        alert("Select Image");

        return;

    }

    const formData = new FormData();

    formData.append("file", imageInput.files[0]);

    result.innerHTML="<h3>Predicting...</h3>";

    try {

        const response = await fetch("https://sentinelai-a6aj.onrender.com/predict", {
            method: "POST",
            body: formData
        });

        console.log(response);

        const data = await response.json();

        console.log(data);

        outputImage.src = data.output_image + "?t=" + Date.now();

        let html = "";

        html += "<h2>Detection Result</h2>";
        html += "<h3>Total Objects : " + data.total_detections + "</h3>";
        html += "<ul>";

        data.detections.forEach(item => {
            html += "<li>" + item.class + " : " + item.confidence + "</li>";
        });

        html += "</ul>";

        result.innerHTML = html;

    } catch (err) {

        console.error(err);

        alert("Unable to connect to FastAPI Backend");

    }
    console.log(data);
    console.log(data.output_image);

    outputImage.src=data.output_image+"?t="+new Date().getTime();

    let html="";

    html+="<h2>Detection Result</h2>";

    html+="<h3>Total Objects : "+data.total_detections+"</h3>";

    html+="<ul>";

    data.detections.forEach(item=>{

        html+="<li>"+item.class+" : "+item.confidence+"</li>";

    });

    html+="</ul>";

    result.innerHTML=html;

});