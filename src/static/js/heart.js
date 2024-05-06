const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const restartBtn = document.getElementById("restartBtn");

function resizeCanvas() {
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;
}
resizeCanvas(); // Set initial size
window.addEventListener('resize', resizeCanvas); // Adjust size on window resize

resizeCanvas(); // Set initial size
window.addEventListener('resize', resizeCanvas); // Adjust size on window resize

const player = { x: 50, y: canvas.height - 50, width: 40, height: 40, velocityY: 0 }; // Player with dynamic position // Increased player size
let obstacles = [];
let gravity = 1.5, jumpPower = -25, score = 0, gameOver = false;
let jumpCount = 0; // To track consecutive jumps
let obstacleFrequency = 0.01; // Starting frequency of obstacles
let obstacleIncreaseRate = 0.00005; // Increase in obstacle frequency over time

// Function to draw the heart shape
function drawHeart(x, y, size) {
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.bezierCurveTo(x, y - size / 2, x - size, y - size / 2, x - size, y);
    ctx.bezierCurveTo(x - size, y + size / 2, x, y + size, x, y + size + size / 2);
    ctx.bezierCurveTo(x, y + size, x + size, y + size / 2, x + size, y);
    ctx.bezierCurveTo(x + size, y - size / 2, x, y - size / 2, x, y);
    ctx.fillStyle = "red";
    ctx.fill();
}

// Draw the player as a heart
function drawPlayer() {
    drawHeart(player.x, player.y, 20); // Doubled the heart size
}

// Create a thinner and more spaced out obstacle
function createObstacle() {
    const height = Math.random() * (canvas.height / 3) + 15; // Reduced max height
    obstacles.push({ x: canvas.width, y: canvas.height - height, width: 35, height: height }); // Reduced obstacle width to 10
}

function drawObstacle() {
    ctx.fillStyle = "darkred"; // Darker color for better visibility
    obstacles.forEach(obs => {
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
    });
}

function drawScore() {
    ctx.fillStyle = "#FFF";
    ctx.font = "24px Arial"; // Larger score font
    ctx.fillText(`Score: ${score}`, 10, 30);
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
        jumpCount = 0; // Reset jump count when on the ground
    }

    // Move and remove obstacles
    obstacles.forEach((obs, index) => {
        obs.x -= 6; // Slightly increased speed
        if (obs.x + obs.width < 0) obstacles.splice(index, 1);
        if (obs.x < player.x + player.width && obs.x + obs.width > player.x &&
            obs.y < player.y + player.height && obs.y + obs.height > player.y) {
            gameOver = true;
            restartBtn.style.display = "block";
        }
    });

    // Increase the obstacle frequency over time
    obstacleFrequency = Math.min(0.005, obstacleFrequency + obstacleIncreaseRate); // Limit maximum frequency

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
    restartBtn.style.display = "none";
    update();
}

// Handle player jump on keyboard press, mouse click, and touch events
function handleJump() {
    if (!gameOver && jumpCount < 3) { // Limit to triple jumps
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

resetGame(); // Start the game initially
