const begin = document.querySelector("#startRec")
var showInfo
var switchFinished
var params

var constrainObj = {
    audio:true,
    video:false
}

function blobToFile(theBlob, fileName){
    //A Blob() is almost a File() - it's just missing the two properties below which we will add
    theBlob.lastModifiedDate = new Date();
    theBlob.name = fileName;
    return theBlob;
}

function initAnim(){
    showInfo = anime.timeline({
        easing:'easeOutQuart',
        autoplay:false
    })

    showInfo.add({
        targets:'#info',
        translateY:[200,0],
        opacity:1,
        duration:500
    })

    switchFinished = anime.timeline({
        easing:'easeOutQuart',
        autoplay:false
    })
    switchFinished.add({
        targets:'#info',
        translateY:[0,200],
        opacity:[1,0],
        duration:500
    })
    switchFinished.add({
        targets:'#done',
        translateY:0,
        opacity:1,
        duration:500
    })
}

window.addEventListener('load', () => {
    params = (new URL(document.location)).searchParams.get("param").split(',')
    initAnim()
    anime.set('#info', {
        translateY:200
    })
    anime.set('#done', {
        translateY:200
    })
})

begin.addEventListener('click', () => {

    navigator.mediaDevices.getUserMedia(constrainObj).then((mediaStreamObj) => {
        showInfo.play()

        // initialize audio capture
        let mediaRecorder = new MediaRecorder(mediaStreamObj)

        chunks = []

        mediaRecorder.start();
        console.log(mediaRecorder.state)

        let done = document.querySelector("#done")
        done.addEventListener('click', () => {
            mediaRecorder.stop()
            console.log(mediaRecorder.state)
        })

        mediaRecorder.ondataavailable = (ev) => {
            chunks.push(ev.data)
        }

        mediaRecorder.onstop = () => {
            let blob = new Blob(chunks, {type : 'audio/wav;'})
            chunks = []

            let url = "results.html?param=" + encodeURIComponent(params)
            let wavFile = blobToFile(blob, '123.wav')
            localStorage.setItem("audio", wavFile)
            window.location = url;
        }

        var countDown = document.querySelector(".count-down")
        setTimeout(() => {
            countDown.innerHTML="2"
        }, 100)
        setTimeout(() => {
            countDown.innerHTML="1"
        }, 200)
        setTimeout(() => {
            countDown.innerHTML="Begin!"
        }, 300)
        setTimeout(() => {
            switchFinished.play()
        }, 400)
    }) .catch(function(err){
        alert("error")
    })

    
})