    function fetchFlowers() {
        fetch('http://127.0.0.1:5000/flowers')
        .then(response => response.json())
        .then(data => {
            let rows = "";
            for (let flowerKey in data) {
                const flower = data[flowerKey];

                let needsWaterClass = flower.water_level < flower.min_water_required ? "needs-water" : "watered";
                let needsWaterText = flower.water_level < flower.min_water_required ? "Yes" : "No";

                rows += `
                <tr class="${needsWaterClass}">
                    <td>${flowerKey}</td>
                    <td>${flower.name}</td>
                    <td>${flower.last_watered}</td>
                    <td>${flower.water_level}</td>
                    <td>${flower.min_water_required}</td>
                    <td>${needsWaterText}</td>
                    <td>
                        <button class="water-btn" onclick="waterFlower(${flowerKey})">Water</button>
                    </td>
                </tr>`;
            }
            document.getElementById("flower-data").innerHTML = rows;
        })
        .catch(error => console.error("Error fetching flowers:", error));
    }

    function addFlower() {
        const name = document.getElementById("flower-name").value;
        const lastWatered = document.getElementById("last-watered").value;
        const waterLevel = document.getElementById("water-level").value;
        const minWaterRequired = document.getElementById("min-water-required").value;

        if (!name || !lastWatered || !waterLevel || !minWaterRequired) {
            alert("Please fill in all fields.");
            return;
        }

        const flowerData = {
            name: name,
            last_watered: lastWatered,
            water_level: parseFloat(waterLevel),
            min_water_required: parseFloat(minWaterRequired)
        };

        fetch('/flower', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(flowerData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchFlowers();  // Refresh the data after adding
        })
        .catch(error => console.error("Error adding flower:", error));
    }

    function waterFlower(flowerId) {
        fetch(`/water/${flowerId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchFlowers();  // Refresh the table after watering
        })
        .catch(error => console.error("Error watering flower:", error));
    }

    // Fetch data on page load
    fetchFlowers();