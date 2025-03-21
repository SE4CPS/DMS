document.addEventListener("DOMContentLoaded", function () {
    const audio = document.getElementById("introMusic");
    const muteButton = document.getElementById("muteButton");

    const playAudio = () => {
        audio.muted = false;
        audio.volume = 1.0;

        // Plays the audio and removes the event listener
        audio.play().then(() => {
            document.body.removeEventListener("click", playAudio);
        });
    };

    // Waits for the user to click anywhere on the page before playing the audio
    document.body.addEventListener("click", playAudio, { once: true });

    // Function to update the mute button icon
    function updateMuteButton() {
        muteButton.textContent = audio.muted ? "\uD83D\uDD07" : "\uD83D\uDD0A";
    }

    updateMuteButton();

    muteButton.addEventListener("click", () => {
        audio.muted = !audio.muted; // Toggles the muted state
        if (!audio.muted) audio.play(); // Plays the audio if it's not muted
        updateMuteButton(); // Toggles the unicode icon
    });
});

// User clicks on the button to show the dropdown options
function dropDown(){
    document.getElementById("dropDownOptions").classList.toggle("show");
}

window.onclick = function(event) {
    if(!event.target.matches('#dropDownButton')){
        let dropdown = document.getElementById("dropDownOptions");
        if(dropdown.classList.contains("show")){
            dropdown.classList.remove("show");
        }
    }
}

// Confirmation before adding a flower
function confirmAddFlower(){
    const flowerName = document.querySelector("input[name='name").value.trim();

        if (!flowerName){
            alert("Please enter a flower name.");
            return false;
        }

        return confirm("Are you sure you want to add this flower?");
}

// Confirmation before deleting a flower
function confirmDeleteFlower(){
    const checkbox = document.querySelectorAll("input[name='selected_flowers']:checked");

    if (checkbox.length === 0){
        alert("Please select at least one flower to delete.");
        return false;
    }

    let selectedFlowerNames = Array.from(checkbox).map(flower => {
        let label = flower.parentElement.textContent.trim();
        return label;
    });

    return confirm(`Are you sure you want to delete the following flowers?\n\n${selectedFlowerNames.join("\n")}`);
}

// Confirmation before watering a selected flower
function confirmWaterFlower(){
    const checkbox = document.querySelectorAll("input[name='selected_flowers']:checked");

    if (checkbox.length === 0){
        alert("Please select at least one flower to water.");
        return false;
    }

    let selectedFlowerNames = [];
    checkbox.forEach((cb) => {
        selectedFlowerNames.push(cb.nextSibling.textContent.trim());
    });

    return confirm(`Are you sure you want to water the following flowers?\n\n${selectedFlowerNames.join("\n")}`);
}

// Function to toggle all checkboxes when "Select All" is clicked
function toggleCheckboxes(selectAllCheckbox) {
    let checkboxes = document.querySelectorAll(".flowerCheckbox");
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
}