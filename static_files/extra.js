if (parameter=="") {
document.getElementById("title").innerText = "E-ink clock";
document.getElementById("content").style['display'] = "none";
document.getElementById("bound").className = "bound";
document.getElementById("bar").style.display = "none";
document.body.style.backgroundColor = "black";
document.body.style.color = "white";
currentTime();
};