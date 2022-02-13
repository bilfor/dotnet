const playerReport = document.createElement('p'); 
const computerReport = document.createElement('p'); 
const gameResult = document.createElement('p');
const winnerMessage = document.createElement('p');
const playerTallyMessage = document.createElement('p');
const computerTallyMessage = document.createElement('p');
const playAgainMessage = document.createElement('p');
const btn1 = document.querySelector('#gb1');
const btn2 = document.querySelector('#gb2');
const btn3 = document.querySelector('#gb3');
const title = document.querySelector('#title');

let playerTally = 0;
let computerTally = 0;

function computerPlay() {
  switch(parseInt(Math.random()*3)) {
    case 0: return 'rock'; break;
    case 1: return 'paper'; break;
    case 2: return 'scissors'; break;
  }
}

function play(playerSelection, computerSelection) {
  playerSelection = playerSelection.toLowerCase();
  computerSelection = computerSelection.toLowerCase();   
  let result = '';

  if (playerSelection == 'rock') {
    switch(computerSelection) {
      case 'rock': result = 'd'; break; 
      case 'paper': result = 'l'; break;
      case 'scissors': result = 'w'; break;
    }
  }

  else if (playerSelection == 'paper') {
    switch(computerSelection) {
      case 'rock': result = 'w'; break; 
      case 'paper': result = 'd'; break;
      case 'scissors': result = 'l'; break;
    }
  }
 
  else if (playerSelection == 'scissors') {
    switch(computerSelection) {
      case 'rock': result = 'l'; break; 
      case 'paper': result = 'w'; break;
      case 'scissors': result = 'd'; break;
    }
  }

  else {
    result='invalid input, game canceled';
  }

  return result;
} 

function judge(result) { 
  if(result == 'w') {
    playerTally++;
  }
  else if(result == 'l') {
    computerTally++;
  }
}

function clearNodes() {
  if(winner.childNodes.length > 1) {
    winner.removeChild(winnerMessage);
  }
}

function printOut(pplay, cplay, result) {
  playerReport.textContent = "You played " + pplay.toUpperCase();
  computerReport.textContent = "Robot played " + cplay.toUpperCase();
  gameResult.textContent = result.toUpperCase();
  results.appendChild(playerReport); 
  results.appendChild(computerReport);
  results.appendChild(gameResult);

  playerTallyMessage.textContent = "YOU: " + playerTally;
  computerTallyMessage.textContent = "ROBOT: " + computerTally;
  score.appendChild(playerTallyMessage); 
  score.appendChild(computerTallyMessage);


  if(playerTally == 5) {
    winnerMessage.textContent = 'GAME OVER! YOU WIN!';
    winner.appendChild(winnerMessage);
    playerTally = 0;
    computerTally = 0;
  }

  else if(computerTally == 5) {
    winnerMessage.textContent = 'GAME OVER! ROBOT WINS!';
    winner.appendChild(winnerMessage);
    playerTally = 0;
    computerTally = 0;
  }

  //playAgainMessage.textContent = "Press any play button to start a new round.";
  //title.appendChild(playAgainMessage);
  

}

btn1.addEventListener('click', function (e) {
  const pplay = 'rock';
  const cplay = computerPlay();
  const result = play('rock', cplay);
  
  clearNodes();
  judge(result);
  printOut('rock',cplay,result);
})

btn2.addEventListener('click', function (e) {
  const pplay = 'paper';
  const cplay = computerPlay();
  const result = play('paper', cplay);

  clearNodes();
  judge(result);
  printOut('paper',cplay,result);
})

btn3.addEventListener('click', function (e) {
  const pplay = 'scissors';
  const cplay = computerPlay();
  const result = play('scissors', cplay);

  clearNodes();
  judge(result);
  printOut('scissors',cplay,result);
})
