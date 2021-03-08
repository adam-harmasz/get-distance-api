function addNewCoordinateField() {
    let currentIndex = 3
    $("#addField").click(
        function (event) {
            if (currentIndex <=50) {
                $("#coordinateFields").append(
                    `
                    <div id="coordinateField-${currentIndex}" class="coordinateField row">
                      <div class="col-md-6">
                        <label for="longitude" class="text-center">Longitude</label>
                        <input type="number" id="longitude" name="longitude" class="form-control longitude" required>
                      </div>
                      <div class="col-md-6">
                        <label for="latitude" class="text-center">Latitude</label>
                        <input type="number" id="latitude" name="latitude" class="form-control latitude" required>
                      </div>
                    </div>
                    `
                )
            } else {
                $("#coordinateFields").append(
                    `
                    <div class="row-form-errors">
                      You've reached limit (50) of coordinates!
                    </div>
                    `
                )
            }
            currentIndex += 1;
        }
    )
}


function groupCoordinates() {
    let input_rows = $(".coordinateField");
    let coordinatesArray = []
    input_rows.each(function (index, element){
        coordinatesArray.push(
            [$(this).find("#latitude").val(), $(this).find("#longitude").val()]
        )
    })
    return coordinatesArray
}


function sendRequest() {
    const resultModal = $("#resultModal")
    $("#sendRequest").click(function (event) {
        clearResults();
        if (isInputsFilled() === 0) {
            resultModal.modal("toggle");
            fetch(
        "http://localhost:8000/total-distance/", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({
                "requestId": $("#requestId").val(),
                "coordinates": groupCoordinates()
                })
            }
        ).then(response => {
            if (response.status === 500) {
                resultModal.modal("hide");
                throw new Error("Unexpected response from server")
            } if (response.status === 400) {
                resultModal.modal("hide");
                response.json().then(function (json){
                    resultModal.modal("hide");
                    throw new Error(json.error)
                }).catch(error => {
                    alert(error);
                })} else
                response.json().then(function (json){
                    resultsModal(json.distance, json.processing_time);
                })

        }).catch(error => {
            alert(error)
        })
        } else
            alert("Some fields are empty");
    })
}


function resultsModal(distance, processing_time) {
    let distanceResultText = "Distance from the given path: " + distance + " meters"
    let durationResultText = "Calculations have been performed in: " + processing_time +  " seconds"
    document.getElementById("distanceResult").innerText = distanceResultText;
    document.getElementById("durationResult").innerText = durationResultText;
}


function clearResults() {
    document.getElementById("distanceResult").innerText = "Waiting ...";
    document.getElementById("durationResult").innerText = "";
}


function fillLongitude() {
    $(".longitude").each(function (index, element) {
        element.value = getRandomIntInclusive(-180, 180)
    })
}

function fillLatitude() {
    $(".latitude").each(function (index, element) {
        element.value = getRandomIntInclusive(-90, 90);
    })
}


function fillFieldsWithSampleData() {
    $("#fillFields").click(function (){
        fillLongitude();
        fillLatitude();
        document.getElementById("requestId").value = "sampleID" + Date.now();
    })
}


function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


function isInputsFilled () {
    return Array.from($("input")).filter( input => input.value === "").length
}


addNewCoordinateField()
sendRequest()
fillFieldsWithSampleData()
