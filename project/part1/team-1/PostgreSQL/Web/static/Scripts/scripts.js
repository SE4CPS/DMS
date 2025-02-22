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

    muteButton.addEventListener("click", () => {
        audio.muted = !audio.muted; // Toggles the muted state
        muteButton.textContent = audio.muted ? "Unmute" : "Mute";   // Changes the button text
        if (!audio.muted) audio.play(); // Plays the audio if it's not muted
    });
});