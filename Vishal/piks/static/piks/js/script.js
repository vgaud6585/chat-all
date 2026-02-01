
// write your script here


// Function to get and display the element's dimensions and styles
var info_div = document.querySelector(".info");
info_div.addEventListener("click",function () {
  info_div.classList.remove("hide");
} );
function displayElementInfo(event) {
  info_div.classList.add("hide");
  
const element = event.target;
var ele_position_top = element.offsetTop;
var ele_position_left = element.offsetLeft;
var page_width = window.innerWidth;
var page_height = window.innerHeight;

// Get computed styles
const style = window.getComputedStyle(element);
const width = element.offsetWidth;
const height = element.offsetHeight;
const margin = `${style.marginTop} ${style.marginRight} ${style.marginBottom} ${style.marginLeft}`;
const padding = `${style.paddingTop} ${style.paddingRight} ${style.paddingBottom} ${style.paddingLeft}`;

// Display the information
const infoDiv = document.getElementById('info');
infoDiv.innerHTML = `
    <strong>Element Info:</strong><br>
    Width: ${width}px<br>
    Height: ${height}px<br>
    Margin: ${margin}<br>
    Padding: ${padding}<br>
    Position: Top ${ele_position_top}px Left ${ele_position_left}<br>
    Page Size: Width ${page_width}px Height ${page_height}
`;
}
// Attach click event to all clickable divs
const clickableDivs = document.querySelectorAll('.clickable');
clickableDivs.forEach(div => {
    div.addEventListener('click', displayElementInfo);
    //clickableDivs.classList.add("mk");
});


function dw(arg) {
  if (typeof(arg) == "object") {
    for (let val in arg) {
      document.write(val + " : " + arg[val] + "<br>");
    }
  } else {
    document.write(arg);
  }
}
//this function is used for add some class in javascript
function class_add(b1,b2) {
  document.querySelector(b1).classList.add(b2);
}