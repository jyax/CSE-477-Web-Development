document.addEventListener('DOMContentLoaded', () => {
	getWordLength(createGameGrid);
})

let wordLength = null
function getWordLength(callback) {
	jQuery.ajax( {
		url: "/getlength",
		type: 'GET',
		success: function(response) {
			wordLength = response.length;
			console.log('Length returned:', wordLength);
			callback(wordLength)
		},
		error :function(err) {
			console.log('Error:', err);
		}
	})
}

function createGameGrid(wordLength) {
	const grid = document.querySelector('.game-grid');
	grid.innerHTML = '';
	grid.style.setProperty('--wordLength', wordLength);
	//grid.style.gridTemplateColumns = `repeat(${wordLength}, auto)`;

	for (let i = 0; i < wordLength; i++) {
        const row = document.createElement('div');
        row.classList.add(`grid-row`);
		row.classList.add(`row${i}`)

        for (let j = 0; j < wordLength; j++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            row.appendChild(cell);
        }

        grid.appendChild(row);
    }
}
let currentGuessNumber = 0;
let currentGuess = [];

document.querySelectorAll('.kb-letter').forEach(button => {
	// Add a click event listener to each letter button
    button.addEventListener('click', () => {
        if (currentGuess.length < wordLength) { // wordLength should be defined and set to the length of the word to guess
            // Update the current guess
            currentGuess.push(button.textContent);
            // Update the display
            updateDisplay();
        }
    });
});

// Function to update the display with the current guess
function updateDisplay() {
    // Select only the cells in the current row
    let currentRowCells = document.querySelectorAll(`.row${currentGuessNumber} .cell`);

    // Clear the display first
    currentRowCells.forEach(cell => cell.textContent = '');

    // Set the letters in the cells based on the current guess
    currentGuess.forEach((letter, index) => {
        if (index < currentRowCells.length) {
            currentRowCells[index].textContent = letter.toUpperCase();
        }
    });
}

document.querySelector('.kb-delete').addEventListener('click', () => {
    // Remove the last letter from the current guess
    currentGuess.pop();
    // Update the display
    updateDisplay();
});

document.querySelector('.kb-enter').addEventListener('click', () => {
    if (currentGuess.length === wordLength) {
        // Submit the guess
        submitGuess();
    } else {
        // Maybe show an error to the user that the guess is too short
        console.error('Guess is not the correct length');
    }
});

document.addEventListener('keydown', (event) => {
    const keyName = event.key.toLowerCase();
	const isLetter = /^[a-z]$/.test(keyName);
    let handled = false;
	event.preventDefault();
    // Check if the key pressed is a letter and add it to the currentGuess
    if (isLetter && currentGuess.length < wordLength) {
        currentGuess.push(keyName);
        updateDisplay();
    } else if (keyName === 'backspace' && currentGuess.length > 0) {
        // Handle backspace
        currentGuess.pop();
        updateDisplay();
    } else if (keyName === 'enter' && currentGuess.length === wordLength) {
        // Handle enter
        submitGuess();
    }
});

// This function would handle the submission of the guess
function submitGuess() {
    // You could use an AJAX call here to send the currentGuess to the server
	let guess = currentGuess.join('').toLowerCase();
	jQuery.ajax( {
		url:"/processguess",
		type: 'POST',
		data: { guess: guess },
		success: function(response) {
			response = JSON.parse(response);
			if (response.correct) {
				let result = new Array(wordLength).fill(2);
				updateGridWithResult(result);
				processEndGame(true);
			} else {
				if(currentGuessNumber+1 >= wordLength) {
					processEndGame(false);
				} else {
					let result = response.result;
					console.log('Returned correctness:', result);
					updateGridWithResult(result);
				}
			}
            currentGuessNumber++;
			currentGuess = [];
		},
		error: function(err) {
			console.log('Error submitting current guess', err);
		}
	})
}

function updateGridWithResult(result) {
    // 0 means absent, 1 means present but in the wrong location, and 2 means correct.
    let currentRow = document.querySelector(`.row${currentGuessNumber}`);
    let cells = currentRow.querySelectorAll('.cell');
	result.forEach((status, index) => {
		let cell = cells[index];
		// Reset classes first if you're reusing cells
		cell.classList.remove('absent', 'letter-present', 'letter-correct');
		switch (status) {
			case 0:
				cell.classList.add('absent');
				break;
			case 1:
				cell.classList.add('letter-present');
				break;
			case 2:
				cell.classList.add('letter-correct');
				break;
		}
	});
}


function processEndGame(win) {
    let score = win ? currentGuessNumber : null;
    let note = win ? `Nice! You beat it in ${currentGuessNumber} guesses.` : "Good try! You didn't get it today.";

    // POST request to submit the score
    jQuery.ajax({
        url: "/processscore",
        type: 'POST',
        data: { score: score },
        success: function() {
            // Once the score is submitted, get the leaderboard
            getLeaderboard(note);
        },
        error: function(err) {
            console.log('Error submitting score:', err);
        }
    });
}

function getLeaderboard(note) {
    jQuery.ajax({
        url: "/processleaderboard",
        type: 'GET',
        success: function(leaderboardData) {
            // Assuming leaderboardData is an array of top 5 scores
            displayLeaderboard(leaderboardData, note);
        },
        error: function(err) {
            console.log('Error getting leaderboard:', err);
        }
    });
}

function displayLeaderboard(leaderboardData, note) {
    const gameContainer = document.querySelector('.game');

    gameContainer.innerHTML = '';

    const noteElement = document.createElement('div');
    noteElement.classList.add('leaderboard-note');
    noteElement.textContent = note;
    gameContainer.appendChild(noteElement);

    const leaderboardElement = document.createElement('div');
    leaderboardElement.classList.add('leaderboard');

    leaderboardData.forEach((entry, index) => {
        const entryElement = document.createElement('div');
        entryElement.classList.add('leaderboard-entry');
        entryElement.textContent = `${index + 1}. ${entry.name} - ${entry.score}`;
        leaderboardElement.appendChild(entryElement);
    })

    gameContainer.appendChild(leaderboardElement);
}