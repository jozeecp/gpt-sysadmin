import Backend from './backend-lib.js';

export class Input {
    constructor() {
        this.line = '';
        this.line_count = 0;
        this.backend = new Backend();
    }

    handler(input) {
        // console.log('User input received: ', input);
        var output = `${input}`;

        if (input === '\r' || input === '\n') {
            // console.log('User pressed enter');
            console.log(this.line);
            if (this.line_count === 0) {
                // send line to backend
                let [human_msg, machine_msg] = this.backend.create_task(this.line);
                output = '\nExplanation: ' + human_msg + '\nassistant@host: ' + machine_msg + '\nuser@host: ';
            }else {
                output = `${input}\nuser@host: `;
            }
            this.line = '';
            this.line_count += 1;
        // check for backspace
        } else if (input.charCodeAt(0) === 127 || input.charCodeAt(0) === 8) {
            console.log('User pressed backspace');
            // remove last character from line
            this.line = this.line.slice(0, -1);
            output = '\b \b';
        } else {
            this.line += input;
        }
        return output;
    }
}

export default Input;