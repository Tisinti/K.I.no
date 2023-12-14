document.addEventListener("DOMContentLoaded", function () {
    let overlay = document.getElementById("overlay");
    let fadeOutInterval;
  
    setTimeout(function () {
      fadeOutInterval = setInterval(function () {
        if (!overlay.style.opacity) {
            overlay.style.opacity = 1;
        }
        if (overlay.style.opacity > 0) {
            overlay.style.opacity -= 0.1;
        } else {
            clearInterval(fadeOutInterval);
            overlay.style.display = "none";
        }
      }, 20);
    }, 2000);
  
    let progressBar = document.getElementById("progressBar");
    let loadingText = document.getElementById("loadingText");
  
    let text = "Loading K.I.no";
    let dots = "";
  
    let animationInterval = setInterval(function () {
        if (dots.length < 3) {
            dots += ".";
        } else {
            dots = "";
        }
        loadingText.textContent = text + dots;
    }, 200);
  
    setTimeout(function () {
        clearInterval(animationInterval);
    }, 2000);

    setTimeout(function () {
        progressBar.style.width = "100%";
    }, 100);
});