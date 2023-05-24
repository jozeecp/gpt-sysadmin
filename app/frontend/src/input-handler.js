import Backend from './backend-lib.js';
import { Terminal } from 'xterm';

// our Terminal class
export class TerminalLib {
    constructor() {
        this.line = '';
        this.line_count = 0;
        this.backend = new Backend();
        this.task_id = '';
        this.terminal = new Terminal();
    }

    // Initialize the terminal
    async init() {
        // Load the terminal
        this.terminal.open(document.getElementById('terminal'));
        // Initialize the terminal
        this.terminal.write(color('Welcome to the GPT-SysAdmin terminal!\r\n', 'cyan'));
        this.terminal.write(color('Please give me a task: ', 'cyan'));
        // Add event listener for onData
        this.terminal.onData(this.handler.bind(this));
    }

    async handler(input) {
        if (input=== '\r' || input === '\n') {
            // if process.env.HOST_ID is not set, tell user to select a host
            if (global.HOST_ID === undefined) {
                this.terminal.write(color('\r\nPlease select a host first!\r\n', 'red'));
                return;
            }


            // Enter key pressed
            this.terminal.write('\r\nLoading...');
            // loading animation
            const loading = ['|', '/', '-', '\\'];
            let i = 4;
            const loadingInterval = setInterval(() => {
                this.terminal.write('\b' + loading[i % 4]);  // Add '\b' to overwrite the previous character
                i++;
            }, 100);
            // Wait a short while before sending the request to the backend
            await new Promise(resolve => setTimeout(resolve, 500));
            
            if (this.line_count === 0) {
                // Send line to backend
                console.log('Sending line to backend');
                const [human_msg, machine_msg, task_id] = await this.backend.create_task(this.line);
                console.log("human_msg", human_msg);
                console.log("machine_msg", machine_msg);
                console.log("task_id", task_id);
                this.task_id = task_id;
                console.log("this.task_id", this.task_id);
                clearInterval(loadingInterval);  // Clear the interval after the request is sent
                this.terminal.write('\b \b');  // Remove the loading character
                // this.terminal.write('\r\nNew Task:' + task_id + '\r\nExplanation: ' + human_msg + '\r\nassistant@host: ' + machine_msg);
                this.terminal.write(color('\r\nNew Task: ', 'green') + task_id + color('\r\nExplanation: ', 'green') + human_msg + color('\r\nassistant@host: ', 'cyan') + machine_msg);
            } else {
                const [human_msg, machine_msg, host_msg] = await this.backend.confirm_step(this.task_id);
                // replace '\n' with '\n\r' for each line in host_msg
                let new_host_msg = host_msg.replace(/\n/g, '\n\r');
                // do the same with human_msg and machine_msg
                let new_human_msg = human_msg.replace(/\n/g, '\n\r');
                let new_machine_msg = machine_msg.replace(/\n/g, '\n\r');
                console.log("human_msg", human_msg);
                console.log("machine_msg", machine_msg);
                console.log("host_msg", new_host_msg);
                clearInterval(loadingInterval);  // Clear the interval after the request is sent
                this.terminal.write('\b \b');  // Remove the loading character
                // this.terminal.write('\r\n' + new_host_msg + '\r\nExplanation: ' + new_human_msg + '\r\nassistant@host: ' + new_machine_msg);
                this.terminal.write('\r\n' + new_host_msg + color('\r\nExplanation: ', 'green') + new_human_msg + color('\r\nassistant@host: ', 'cyan') + new_machine_msg);
            }
            
            this.line_count += 1;  // Increment line count after the command is processed
            this.line = '';  // Clear the line for the next command
        } else if (input.charCodeAt(0) === 127) {
            // backspace
            this.terminal.write('\b \b');
            this.line = this.line.slice(0, -1);
        }
        else {
            this.terminal.write(input);
            this.line += input;
        }
    }
    
}


function color(text, color) {
    // the terminal prints text in color based on the color code
    // color codes are defined in the color_code dictionary
    // e.g., color('hello', 'red') will print 'hello' in red
    // and return '\x1b[31mhello\x1b[0m'

    const color_code = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36
    }[color];
    return `\x1b[${color_code}m${text}\x1b[0m`;
}


export default TerminalLib;
