function addNewCoordinateField() {
    let currentIndex = 3
    $("#addField").click(
        function (event) {
            if (currentIndex <=50) {
                $("#coordinateFields").append(
                    `
                    <div id="coordinateField-${currentIndex}" class="coordinateField row">
                      <div class="col-md-6">
                        <label for="longitude" class="text-center">Longtitude</label>
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
    input_rows.each(function (index){
        coordinatesArray.push(
            [$(this).find("#longitude").val(), $(this).find("#latitude").val()]
        )
    })
    return coordinatesArray
}


function sendRequest() {
    $("#sendRequest").click(function (event) {
        fetch(
            "http://localhost:8000/total-distance/", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                "requestId": $("#requestId").val(),
                "coordinates": groupCoordinates()})
            }
        ).then(response => {
            console.log(response);
        }).catch(error => {
            console.log("Error: " + error)
        })
    })
}


addNewCoordinateField()
sendRequest()
