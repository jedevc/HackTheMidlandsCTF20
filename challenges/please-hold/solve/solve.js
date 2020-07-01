var md5 = require("blueimp-md5");

var base = 7594653;
var base_flag = "INITIAL_VALUE";

var value = base;
var value_flag = base_flag;

while (value > 0) {
  value -= 1;
  value_flag = md5(value_flag);
}
console.log("HTM{" + value_flag + "}");
