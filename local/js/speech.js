const begin = document.querySelector("#startRec")
var showInfo
var switchFinished

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
    const params = (new URL(document.location)).searchParams.get("param").split(',')
    initAnim()
    anime.set('#info', {
        translateY:200
    })
    anime.set('#done', {
        translateY:200
    })
})

begin.addEventListener('click', () => {
    showInfo.play()
    var countDown = document.querySelector(".count-down")
    setTimeout(() => {
        countDown.innerHTML="2"
    }, 1000)
    setTimeout(() => {
        countDown.innerHTML="1"
    }, 2000)
    setTimeout(() => {
        countDown.innerHTML="Begin!"
    }, 3000)
    setTimeout(() => {
        switchFinished.play()
    }, 4000)
})