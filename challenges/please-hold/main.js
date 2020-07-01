window.addEventListener("DOMContentLoaded", function () {
  var initialCounter = 7594653;
  var initialFlag = "INITIAL_VALUE";

  var counter = initialCounter;
  var flag = initialFlag;

  var counterEl = document.getElementById("counter");
  var flagEl = document.getElementById("flag");

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
      if (counter <= 0) {
        flagEl.innerHTML = "HTM{" + flag + "}";
      } else {
        counter -= 1;
        flag = md5(flag);
      }
    } else {
      counter = initialCounter;
      flag = initialFlag;
    }
    counterEl.innerHTML = counter;
  }
  setInterval(update, 1000);
  update();
});
