import Backend from './backend-lib.js';

export class Input {
    constructor() {
        this.line = '';
        this.line_count = 0;
        this.backend = new Backend();
    }

    async handler(input) {
        // console.log('User input received: ', input);
        var output = `${input}`;

        if (input === '\r' || input === '\n') {
            console.log('User pressed enter');
            console.log('Line: ', this.line);
            if (this.line_count === 0) {
                // Send line to backend
                console.log('Sending line to backend');
                const [human_msg, machine_msg] = await this.backend.create_task(this.line);
                console.log("human_msg", human_msg);
                console.log("machine_msg", machine_msg);
                output = '\n\rExplanation: ' + human_msg + '\n\rassistant@host: ' + machine_msg;
            } else {
                output = `${input}\nuser@host: `;
            }
            this.line = '';
            this.line_count += 1;
        // Check for backspace
        } else if (input.charCodeAt(0) === 127 || input.charCodeAt(0) === 8) {
            console.log('User pressed backspace');
            // Remove last character from line
            this.line = this.line.slice(0, -1);
            output = '\b \b';
        } else {
            this.line += input;
        }
        return output;
    }
}

export default Input;
