const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const restartBtn = document.getElementById("restartBtn");
const startBtn = document.getElementById("startBtn");

restartBtn.style.display = "none";

startBtn.addEventListener("click", startGame);

function startGame() {
  startBtn.style.display = "none";
  restartBtn.style.display = "block";
  gameOver = false;
  resetGame();
}

function resizeCanvas() {
  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

const player = {
  x: 50,
  y: canvas.height - 50,
  width: 40,
  height: 40,
  velocityY: 0,
};
let obstacles = [];
let gravity = 1.5,
  jumpPower = -25,
  score = 0,
  gameOver = true;
let jumpCount = 0;
let obstacleFrequency = 0.01;
let obstacleIncreaseRate = 0.00005;

const overlapBuffer = 7;

function checkCollision(player, obs) {
  return (
    obs.x + overlapBuffer < player.x + player.width - overlapBuffer &&
    obs.x + obs.width - overlapBuffer > player.x + overlapBuffer &&
    obs.y + overlapBuffer < player.y + player.height - overlapBuffer &&
    obs.y + obs.height - overlapBuffer > player.y + overlapBuffer
  );
}

// Function to draw the heart shape
function drawHeart(x, y, size) {
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.bezierCurveTo(x, y - size / 2, x - size, y - size / 2, x - size, y);
  ctx.bezierCurveTo(
    x - size,
    y + size / 2,
    x,
    y + size,
    x,
    y + size + size / 2,
  );
  ctx.bezierCurveTo(x, y + size, x + size, y + size / 2, x + size, y);
  ctx.bezierCurveTo(x + size, y - size / 2, x, y - size / 2, x, y);
  ctx.fillStyle = "red";
  ctx.fill();
}

// Draw the player as a heart
function drawPlayer() {
  drawHeart(player.x, player.y, 20);
}

function createObstacle() {
  const height = Math.random() * (canvas.height / 3) + 15;
  obstacles.push({
    x: canvas.width,
    y: canvas.height - height,
    width: 35,
    height: height,
  });
}

function drawObstacle() {
  ctx.fillStyle = "darkred";
  obstacles.forEach((obs) => {
    ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
  });
}

function drawScore() {
  ctx.font = "14px Arial";
  ctx.fillStyle = "#FFF";
  let scoreText = `Score: ${score}`;

  if (gameOver) {
    // Center score on game over
    ctx.font = "30px Arial";
    let textWidth = ctx.measureText(scoreText).width;
    let xPosition = (canvas.width - textWidth) / 2;
    let yPosition = canvas.height / 2;
    ctx.fillText(scoreText, xPosition, yPosition);
  } else {
    ctx.font = "14px Arial";
    // Display score at the top left corner during gameplay
    ctx.fillText(scoreText, 10, 30);
  }
}

function update() {
  if (gameOver) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Player physics
  player.velocityY += gravity;
  player.y += player.velocityY;

  // Check if player lands on the ground
  if (player.y + player.height > canvas.height) {
    player.y = canvas.height - player.height;
    player.velocityY = 0;
    jumpCount = 0;
  }

  // Move and remove obstacles
  obstacles.forEach((obs, index) => {
    obs.x -= 6; // Example speed adjustment
    if (obs.x + obs.width < 0) obstacles.splice(index, 1);

    if (checkCollision(player, obs)) {
      gameOver = true;
      restartBtn.style.display = "block";
    }
  });

  // Increase the obstacle frequency over time
  obstacleFrequency = Math.min(0.005, obstacleFrequency + obstacleIncreaseRate);

  // Score and new obstacles
  if (Math.random() < obstacleFrequency) createObstacle();
  score++;

  // Draw
  drawPlayer();
  drawObstacle();
  drawScore();

  requestAnimationFrame(update);
}

function resetGame() {
  player.x = 50;
  player.y = 180;
  player.velocityY = 0;
  obstacles = [];
  score = 0;
  gameOver = false;
  jumpCount = 0; // Reset jump count
  obstacleFrequency = 0.0005; // Reset to starting frequency
  update();
}

// Handle player jump on keyboard press, mouse click, and touch events
function handleJump() {
  if (!gameOver && jumpCount < 3) {
    player.velocityY = jumpPower;
    jumpCount++;
  }
}

window.addEventListener("keydown", (e) => {
  if (e.key === " " || e.key === "ArrowUp") {
    e.preventDefault();
    handleJump();
  }
});

canvas.addEventListener("click", handleJump);
canvas.addEventListener("touchstart", handleJump);

restartBtn.addEventListener("click", resetGame);
