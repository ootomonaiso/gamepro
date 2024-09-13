async function startAutoPlay() {
    const response = await fetch('/api/start_auto_play', {
        method: 'POST',
    });
    const data = await response.json();
    renderBoard(data.board, data.score);
    if (data.game_over) {
        document.getElementById('status').textContent = 'ステータス: ゲームオーバー';
    }
}

async function automateStep() {
    const response = await fetch('/api/automate_step', {
        method: 'POST',
    });
    const data = await response.json();
    renderBoard(data.board, data.score);
    if (data.game_over) {
        document.getElementById('status').textContent = 'ステータス: ゲームオーバー';
    }
}

function renderBoard(board, score) {
    const container = document.getElementById('game-container');
    container.innerHTML = '';
    board.forEach(row => {
        row.forEach(cell => {
            const tile = document.createElement('div');
            tile.className = `tile tile-${cell}`;
            tile.textContent = cell !== 0 ? cell : '';
            container.appendChild(tile);
        });
    });
    document.getElementById('score').textContent = `Score: ${score}`;
}

// 自動プレイの更新を行う
setInterval(automateStep, 1000);  // 1秒ごとに次のステップを実行
