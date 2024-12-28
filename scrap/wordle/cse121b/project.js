/*
    Bryant Smith
    BYU-I CSE 121B
    W6 Task Project
    27 May 2023
    project.js
*/

// Game Object
const game = {
    active: {round: 0, letter: 0},
    dimensions: {width: 5, height: 6},
    elements: {
        gameRows: document.getElementById("game-rows"),
        selection: document.getElementById("selection"),
        wrapper: document.getElementById("wrapper")
    }
};

// Functions
async function startGame() {

    async function fetchWord() {
        
        const url = "https://random-word-api.vercel.app/api?words=1&length=5";
        let response = await fetch(url);
        if (response.ok) {
            let array = await response.json();
            let word = array[0];
            let answer = word.split("");
            return answer;
        } else {alert("Failed to fetch response from random word API.");}
    }

    game.answer = await fetchWord();
    displayGame();
}

function displayGame() {
    
    function newElement(label, counter, parent, inherit_parent_id=true) {
        let element = document.createElement("div");
        let id = label[0].concat(counter.toString());
        if (inherit_parent_id) {element.id = parent.id.concat(id);}
        else {element.id = id;}
        element.classList.add(label);
        parent.appendChild(element);
        return element;
    }

    function displayRows(parent) {
        for (i = 0; i < game.dimensions.height; i++) {
            let rowElement = newElement("round", i, parent, false);
            displayColumns(rowElement);
        }
    }

    function displayColumns(parent) {
        for (j = 0; j < game.dimensions.width; j++) {
            let columnElement = newElement("letter", j, parent, true);
            columnElement.classList.add("unused")
        }
    }

    function initializeKeyboard() {
        game.keyCodes = [];
        for (i = 65; i <= 90; i++) {
            let eventCode = "Key".concat(String.fromCharCode(i));
            game.keyCodes.push(eventCode)
        }
        for (i = 97; i <= 122; i++) {
            let keyElement = document.getElementById(String.fromCharCode(i));
            keyElement.removeAttribute("class");
            keyElement.classList.add("keys", "unused");
        }
    }
    
    game.elements.gameRows.innerHTML = "";
    displayRows(game.elements.gameRows);
    initializeKeyboard();
    playGame();
}

function playGame() {
    
    function getId() {
        let id =
            "r" + game.active.round.toString() +
            "l" + game.active.letter.toString();
        return id;
    }

    function activateElement() {
        if (game.active.letter < game.dimensions.width) {
            let activeId = getId();
            game.active.element = document.getElementById(activeId);
            listen();
        } else {awaitSubmission();}
    }

    function listen() {
        document.addEventListener("keydown", (event) => {
            if (game.keyCodes.includes(event.code)) {writeInput(event);}
            else if (event.code == "Backspace") {
                if (game.active.letter > 0) {deleteLast();}
                else {listen();}
            } else if (event.code == "ShiftLeft" || event.code == "ShiftRight") {
                listen()
            }
            else {
                alert(
                    "Please type letters, Backspace to undo, or Enter to submit complete word."
                );
                listen();
            }
        }, {once: true});
    }
    
    function writeInput(event) {
        game.active.element.innerHTML = `${event.key.toUpperCase()}`;
        game.active.letter++;
        activateElement();
    }

    function deleteLast() {
        game.active.letter--;
        let targetId = getId();
        document.getElementById(targetId).innerHTML = "";
        activateElement();
    }

    function awaitSubmission() {
        document.addEventListener("keydown", (event) => {
            if (event.code == "Enter" || event.code == "NumpadEnter") {
                readGuess();
            } else if (event.code == "Backspace") {deleteLast();}
            else {
                alert("Please press Enter to submit, or Backspace to modify.");
                awaitSubmission();
            }
        }, {once: true});
    }

    function readGuess() {
        let guess = [];
        for (
            game.active.letter = 0;
            game.active.letter < game.dimensions.width;
            game.active.letter++
        ) {
            let letterId = getId();
            let letter = 
                document.getElementById(letterId).innerText.toLowerCase();
            guess.push(letter);
        }
        evaluate(guess);
    }

    function evaluate(guess) {
        game.score = 0;
        for (
            game.active.letter = 0;
            game.active.letter < game.dimensions.width;
            game.active.letter++
        ) {
            let status = determineStatus(guess);
            updateClass(status);
            if (status === "match") {game.score++}
        }
        game.active.round++
        if (gameOver(game.score)) {endgame();}
        else {
            game.active.letter = 0;
            activateElement();
        }
    }

    function determineStatus(guess) {
        let i = game.active.letter;
        let status;
        if (guess[i] === game.answer[i]) {status = "match";}
        else if (game.answer.includes(guess[i])) {status = "within";}
        else {status = "used";}
        return status;
    }

    function updateClass(status) {
        let boxId = getId();
        let boxElement = document.getElementById(boxId);
        boxElement.classList.add(status);
        let letterId = boxElement.innerText.toLowerCase();
        let keyElement = document.getElementById(letterId);
        keyElement.classList.add(status);
    }

    function gameOver(score) {
        if (score === game.dimensions.width) {game.win = true;}
        else if (game.active.round === game.dimensions.height) {
            game.win = false;
        } else {return false;}
        return true;
    }

    activateElement();
}

function endgame() {
    if (game.win) {game.elements.wrapper.classList.add("win");}
    else {game.elements.wrapper.classList.add("lose");}
}

// Execution
startGame();
