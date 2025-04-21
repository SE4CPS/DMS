function applyWaterLoss() {
    if (confirm('Are you sure you want to apply water loss?')) {
        fetch('/team2_flowers_water_loss', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                alert('Water loss simulation applied successfully!');
                window.location.reload();
            } else {
                alert('Failed to apply water loss simulation.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while applying water loss simulation.');
        });
    }
}

function deleteFlower(flowerId) {
    if (confirm('Are you sure you want to delete this flower?')) {
        fetch(`/delete_flower/${flowerId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                alert('Flower deleted successfully!');
                window.location.reload(); 
            } else {
                alert('Failed to delete the flower.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the flower.');
        });
    }
}

function waterFlower(flowerId) {
    const newWaterLevel = prompt('Enter the new water level:');
    if (newWaterLevel !== null && !isNaN(newWaterLevel)) {
        const formData = new FormData();
        formData.append('flower_id', flowerId);
        formData.append('water_level', newWaterLevel);

        fetch('/water_flowers', {
            method: 'POST',
            body: formData, 
        })
        .then(response => {
            if (response.ok) {
                alert('Flower watered successfully!');
                window.location.reload();
            } else {
                alert('Failed to water the flower');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while watering the flower.');
        });
    }
}
