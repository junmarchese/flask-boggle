class BoggleGame {

    constructor(boardId, secs = 60) {
        this.secs = secs;
        this.displayTimer();

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".word-form", this.board).on("submit", this.handleSubmit.bind(this));
    }

    /* display word in the list of found words */

    displayWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
    }

    /* display score in html */

    displayScore() {
        $(".score", this.board).text(this.score);
    }

    /* display status message */

    displayMessage(msg, clss) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${clss}`);
    }

    /* handle word submission */

    async handleSubmit(e) {
        e.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
                this.displayMessage("Word already exists!", "err");
                return;
        }

        const response = await axios.get("/check-word", { params: { word: word }});
        if (response.data.result === "not-a-word") {
            this.displayMessage(`${word} is not a valid English word`, "err");
        } else if (response.data.result === "not-on-board") {
            this.displayMessage(`${word} is not a valid word on this board`, "err");
        } else {
            this.displayWord(word);
            this.score += word.length;
            this.displayScore();
            this.words.add(word);
            this.displayMessage(`${word} is valid and on this board!`, "ok");
        }

        $word.val("").focus();
    }

    displayTimer() {
        $(".timer", this.board).text(this.secs);
    }

    /* handle a second game */

    async tick() {
        this.secs -= 1;
        this.displayTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreBoggleGame();
        }
    }

    /* game ends, score and update message */

    async scoreBoggleGame() {
        $(".word-form", this.board).hide();
        const response = await axios.post("/post-score", { score: this.score });
        if (response.data.newBestScore) {
            this.displayMessage(`New Best Score: ${this.score}`, "ok");
        } else {
            this.displayMessage(`Your Final Score: ${this.score}`, "ok");
        }
    }
}

