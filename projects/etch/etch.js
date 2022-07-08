const drawspace = document.querySelector('#drawspace'); 

function createBox(i, dim) {
  const box = document.createElement('div');
  box.textContent = " ";
  box.style = "background-color: #FFFDD0; flex: 1 0 " + dim + "%; height: " + dim + "%;"; 
  box.setAttribute("class", "box"); 
  box.setAttribute("id", "box" + i);
  drawspace.appendChild(box);
  
  box.addEventListener("mouseenter", function(event) {
    event.target.style.backgroundColor = "#4B4E53";
  })
}

function createGrid(size) {
  const dim = 100/Math.sqrt(size);
  for (let i = 0; i < size; i++) {
    createBox(i, dim);
  }
}

function noChildren(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
} 

function reset() {
  let size = 101; 
  while(size > 100) {
    size = prompt("New size? (ex: '3' -> new 3x3 grid) MAX = 100");
  }
  noChildren(drawspace);
  createGrid(size*size);
}

createGrid(16*16);
