const nextBtn = document.querySelector("#cont")
const phraseKey = []

nextBtn.addEventListener('click', () => {
    phrases = document.querySelector("#phrases").value;
    let url = "speech.html?param=" + encodeURIComponent(phrases).replaceAll('%20', '')
    window.location = url;
})