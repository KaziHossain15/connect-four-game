// script.js
document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('board');
    const rows = 6;
    const cols = 7;
    let currentPlayer = 'red';

    function createBoard() {
        board.innerHTML = '';
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                cell.dataset.row = row;
                cell.dataset.col = col;
                cell.addEventListener('click', handleClick);
                board.appendChild(cell);
            }
        }
    }

    function handleClick(event) {
        const cell = event.target;
        const col = parseInt(cell.dataset.col);
        const cellsInColumn = Array.from(document.querySelectorAll(`.cell[data-col="${col}"]`));
        
        for (let i = cellsInColumn.length - 1; i >= 0; i--) {
            const c = cellsInColumn[i];
            if (!c.classList.contains('red') && !c.classList.contains('yellow')) {
                c.classList.add(currentPlayer);
                if (checkWin()) {
                    alert(`${currentPlayer.toUpperCase()} wins!`);
                    return;
                }
                currentPlayer = currentPlayer === 'red' ? 'yellow' : 'red';
                break;
            }
        }
    }

    function checkWin() {
        const cells = Array.from(document.querySelectorAll('.cell'));
        const winningCombinations = [
            // Horizontal
            [[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]],
            // Vertical
            [[0, 7, 14, 21], [1, 8, 15, 22], [2, 9, 16, 23], [3, 10, 17, 24], [4, 11, 18, 25], [5, 12, 19, 26]],
            // Diagonal (down-right)
            [[0, 8, 16, 24], [1, 9, 17, 25], [2, 10, 18, 26], [3, 11, 19, 27]],
            // Diagonal (up-right)
            [[21, 15, 9, 3], [22, 16, 10, 4], [23, 17, 11, 5], [24, 18, 12, 6]],
        ];

        for (let combo of winningCombinations) {
            for (let sequence of combo) {
                const [a, b, c, d] = sequence;
                if (
                    cells[a].classList.contains(currentPlayer) &&
                    cells[b].classList.contains(currentPlayer) &&
                    cells[c].classList.contains(currentPlayer) &&
                    cells[d].classList.contains(currentPlayer)
                ) {
                    return true;
                }
            }
        }
        return false;
    }

    function resetBoard() {
        createBoard();
        currentPlayer = 'red';
    }

    createBoard();
});
