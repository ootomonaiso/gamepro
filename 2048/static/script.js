async function move(direction) {
    const response = await fetch('/api/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction }),
    });
    const data = await response.json();
    if (data.game_over) {
        // ゲームオーバー時に結果ページにリダイレクト
        showGameOver(data.state);
    } else {
        renderBoard(data.state.board, data.state.score);
    }
}

// ゲームオーバー時にリダイレクトする関数
function showGameOver(state) {
    const score = state.score; // スコアを取得
    window.location.href = `/result?score=${score}`;
}

// ゲームのボードを描画する関数
function renderBoard(board, score) {
    const container = document.getElementById('game-container');
    const scoreElement = document.getElementById('score');
    
    container.innerHTML = '';
    board.forEach(row => {
        row.forEach(cell => {
            const tile = document.createElement('div');
            tile.className = `tile tile-${cell}`;
            tile.textContent = cell !== 0 ? cell : '';
            container.appendChild(tile);
        });
    });

    // スコアを更新
    scoreElement.textContent = `Score: ${score}`;
}

// キー入力イベントの設定
document.addEventListener('keydown', (event) => {
    let direction;
    switch (event.key) {
        case 'ArrowUp':
            direction = 'up';
            break;
        case 'ArrowDown':
            direction = 'down';
            break;
        case 'ArrowLeft':
            direction = 'left';
            break;
        case 'ArrowRight':
            direction = 'right';
            break;
        default:
            return; // 他のキーは無視
    }
    move(direction);
});

// ゲームのリセット
async function resetGame() {
    const response = await fetch('/api/reset', {
        method: 'POST',
    });
    const data = await response.json();
    renderBoard(data.board, data.score);
}

// ページが読み込まれたときにゲームをリセット
window.onload = resetGame;
