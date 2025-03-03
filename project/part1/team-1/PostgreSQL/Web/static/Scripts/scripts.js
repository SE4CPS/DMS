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