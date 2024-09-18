const initApp = () =>{
    const container = document.getElementById("container")
    const secondContainer = document.getElementById("second__container")
    const secondContainerLink = document.getElementById("second__container__link")
    const containerLink = document.getElementById("container__link")
    const audio = document.querySelector("audio")
    const musicName = document.getElementById("music__name")
    const title = document.querySelectorAll(".music__title")
    const line = document.getElementById("line")
    const smallCircle = document.getElementById("small__circle")
    const disk = document.getElementById("disk")
    const previous = document.getElementById("prev__btn")
    const playState = document.getElementById("play__state")
    const next = document.getElementById("next__btn")
    const musicList = []
    const hide  = document.getElementById("hide")



    secondContainerLink.addEventListener("click", () => {
        secondContainer.style.display = "none";
        container.style.display = "block";
    })

    containerLink.addEventListener("click", () => {
        secondContainer.style.display = "block";
        container.style.display = "none";
    })


    

    title.forEach(title => {
        let name = title.innerText
        name.replace(" ","")
       musicList.push(name)
    })

    previous.addEventListener("click", () =>{
        const name = musicName.innerText;
        let nameValue = musicList.indexOf(name);
        let newNameValue = musicList[nameValue - 1]
        if(nameValue == -1){
            alert("Music Does Not exist")
        }
        else if(newNameValue == undefined){
            alert("No Next Music to play, Please add or choose from the playlist")
        }
        else{
        newNameValue.replace(" ","")
        audio.src =  `/static/media/${newNameValue}`;
        musicName.innerText = newNameValue;
        audio.load()
        audio.play();
        line.style.animationDuration = audio.duration;
        smallCircle.style.animationDuration = audio.duration;
        disk.style.animationDuration = audio.duration;
        line.style.animationPlayState = 'running';
        smallCircle.style.animationPlayState = 'running';
        disk.style.animationPlayState = 'running';
        }

    })

    next.addEventListener("click", () =>{
        const name = musicName.innerText;
        let nameValue = musicList.indexOf(name);
        let newNameValue = musicList[nameValue + 1]
        if(nameValue == -1){
            alert("Music Does Not exist")
        }
        else if(newNameValue == undefined){
            alert("No Next Music to play, Please add or choose from the playlist")
        }
        else{
        newNameValue.replace(" ","")
        audio.src =  `/static/media/${newNameValue}`;
        musicName.innerText = newNameValue;
        audio.load()
        audio.play();
        line.style.animationDuration = audio.duration;
        smallCircle.style.animationDuration = audio.duration;
        disk.style.animationDuration = audio.duration;
        line.style.animationPlayState = 'running';
        smallCircle.style.animationPlayState = 'running';
        disk.style.animationPlayState = 'running';
        }

    })


    title.forEach(title => {
        title.addEventListener("click", () =>{
            secondContainer.style.display = "none";
            container.style.display = "block";
            musicName.innerText = title.innerText;
            musicName.innerText.replace(" ","")
            audio.src =  `/static/media/${musicName.innerText}`;
            audio.load()
            audio.play()
            audio.addEventListener("loadedmetadata", ()=>{
                line.style.animationDuration = audio.duration + "s";
                smallCircle.style.animationDuration = audio.duration + "s";
                disk.style.animationDuration = audio.duration + "s";
                line.style.animationPlayState = 'running';
                smallCircle.style.animationPlayState = 'running';
                disk.style.animationPlayState = 'running';
            })
            
            
            

        })
    })
    playState.addEventListener("click", () =>{
        
       if(audio.paused){
            line.style.animationPlayState = 'running';
            smallCircle.style.animationPlayState = 'running';
            disk.style.animationPlayState = 'running';
            audio.play();
            playState.innerHTML = `<i class="fa-solid fa-play"></i>`;
        }
       else if(audio.played){
            line.style.animationPlayState = 'paused';
            smallCircle.style.animationPlayState = 'paused';
            disk.style.animationPlayState = 'paused';
            audio.pause()
            playState.innerHTML = `<i class="fa-solid fa-pause"></i>`;

        }
    })


    line.style.animationPlayState = 'paused';
    smallCircle.style.animationPlayState = 'paused';
    disk.style.animationPlayState = 'paused';
}

window.addEventListener("DOMContentLoaded", initApp)

