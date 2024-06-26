
var airports = { airports , tojson };

function updateDestinations() {
    var selectedSource = document.getElementById("Source").value;
    var destinationDropdown = document.getElementById("Destination");

    // Clear existing options
    destinationDropdown.innerHTML = "";

    // Add all airports to the destination dropdown exvar airports = {{ airports | tojson }};cept the selected source
    for (var i = 0; i < airports.length; i++) {
        var airport = airports[i];
        if (airport !== selectedSource) {
            var option = document.createElement("option");
            option.value = airport;
            option.text = airport;
            destinationDropdown.appendChild(option);
        }
    }
}

    // Call the updateDestinations function when the page loads and when the source dropdown changes
window.onload = updateDestinations;
document.getElementById("Source").onchange = updateDestinations;
