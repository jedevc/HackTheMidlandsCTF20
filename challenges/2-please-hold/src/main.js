window.addEventListener("DOMContentLoaded", function () {
  var initialCounter = 1337133713371337;
  var counter = initialCounter;

  var flagEl = document.getElementById("flag");
  var counterEl = document.getElementById("counter");

  var clicked = false;
  function mouseDown() {
    clicked = true;
  }
  function mouseUp() {
    clicked = false;
  }
  window.addEventListener("mousedown", mouseDown);
  window.addEventListener("mouseleave", mouseUp);
  window.addEventListener("mouseout", mouseUp);
  window.addEventListener("mouseup", mouseUp);

  function update() {
    if (clicked) {
      if (counter == 0) {
        fetch("/flag/" + counter.toString() + initialCounter.toString()).then(function(response) {
          response.text().then(function(text) {
            flagEl.innerHTML = text
          })
        })
      } else {
        counter -= 1;
      }
    } else {
      counter = initialCounter;
    }
    counterEl.innerHTML = counter;
  }
  setInterval(update, 1000);
  update();
});
