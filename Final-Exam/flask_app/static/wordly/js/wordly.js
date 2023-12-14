function createGameGrid(wordLength) {
	const grid = document.getElementsByClassName('game-grid');
	grid.style.gridTemplateColumns = `repeat(${wordLength}, auto)`;

	for (let i = 0; i < wordLength * wordLength; i++) {
		const cell = document.createElement('div');
		cell.classList.add('cell');
		grid.appendChild(cell);
	}
}
function createGame() {
	const word_length = getWordOfTheDay();
	createGameGrid(daily_word.length)
}


let enterButton = document.querySelector('.kb-letter-enter');
enterButton.addEventListener('click', () => {
	console.log('Wordly enter button clicked')

});