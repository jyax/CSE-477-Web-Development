const keys = document.querySelectorAll('.white-key, .black-key');
keys.forEach((key) => {
    key.addEventListener('mouseover', () => {
        console.log(`Mouseover: ${key.id}`);
    });
});

const notes = document.querySelectorAll('.note');

document.getElementById('keyboard').addEventListener('mouseover', () => {
    notes.forEach(note => {
        note.style.display = 'block';
    });
});

document.getElementById('keyboard').addEventListener('mouseout', () => {
    notes.forEach(note => {
        note.style.display = 'none';
    });
});

// Sound Map
const sound = {97:"https://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    119:"https://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    115:"https://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    101:"https://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    100:"https://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    102:"https://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    116:"https://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    103:"https://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    121:"https://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    104:"https://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    117:"https://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    106:"https://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    107:"https://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    111:"https://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    108:"https://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    112:"https://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    59:"https://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"};

// Create an audio element to play the sound
let audio = new Audio();

const secretSequence = 'weseeyou';
let typedKeys='';

function keydownHandler(event) {
    const pressedKey = event.key;

    const isNote = document.getElementById(pressedKey);
    typedKeys += pressedKey;
    console.log(`typedKeys: ${typedKeys}`);

    if (isNote) {
        isNote.classList.add('pressed');
        console.log(`Keydown: ${pressedKey}`);

        // Get the Unicode code of the pressed key
        const keyUnicode = pressedKey.charCodeAt(0);
        console.log(`KeyUnicode: ${keyUnicode}`);
        console.log(`Sound: ${sound[keyUnicode]}`);
        // Check if a sound URL is found
        if (sound[keyUnicode]) {
            console.log(`Key is a note: ${keyUnicode}`);
            // Set the audio element's source to the sound URL
            audio.src = sound[keyUnicode];


            let current_key = document.getElementById(`${pressedKey}`);

            function randInt(min, max) {
                min = Math.ceil(min);
                max = Math.floor(max);
                return Math.floor(Math.random() * (max - min + 1) + min); // Include max value
            }

            // Generate random HSL color
            let hue = randInt(0, 255);
            let saturation = 100; // You can adjust this value
            let lightness = 50; // You can adjust this value
            let alpha = 1; // Alpha (transparency)

            // Construct the HSL color string
            let hslColor = `hsl(${hue}, ${saturation}%, ${lightness}%, ${alpha})`;

            // Set the background color of the element
            current_key.style.backgroundColor = hslColor;

            // Play the sound and handle the Promise
            audio.play()
                .then(() => {
                    // Playback started successfully
                    console.log(`Sound for key ${pressedKey} started.`);
                })
                .catch((error) => {
                    // Handle any errors during playback
                    console.error(`Error playing sound for key ${pressedKey}: ${error}`);
                });
        }
    }

    if (typedKeys.includes(secretSequence)) {
        console.log('Secret Message typed');
        ariseGreatOldOne();
    }
}

function keyupHandler(event) {
    const releasedKey = event.key;

    const isNote = document.getElementById(releasedKey);

    if (isNote) {
        isNote.classList.remove('pressed');
        console.log(`Keyup: ${releasedKey}`);

        let current_key = document.getElementById(`${releasedKey}`);

    // Construct the HSL color string
        if (current_key.classList.contains('white-key')) {
            current_key.style.backgroundColor = "white";
        } else {
            current_key.style.backgroundColor = "black";
        }

    }
}

document.addEventListener('keydown', keydownHandler);
document.addEventListener('keyup', keyupHandler);

function ariseGreatOldOne() {
    const piano = document.getElementById('piano');
    const texture = document.getElementById('texture');
    const creepyAudio = document.getElementById('creepy-audio');

    piano.style.transition = 'opacity 3s';
    piano.style.opacity = '0';
    piano.style.pointerEvents = 'none';

    texture.style.transition = 'opacity 3s';
    texture.style.opacity = '1';
    texture.style.display = 'block';

    document.removeEventListener('keydown', keydownHandler);
    document.removeEventListener('keyup', keyupHandler);

    creepyAudio.play();
}