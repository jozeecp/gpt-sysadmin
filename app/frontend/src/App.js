import Input from './input-handler';
import React from 'react';
import ReactDOM from 'react-dom';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';
import './styles.css';

class App extends React.Component {
    componentDidMount() {
        // Initialize the terminal
        this.terminal = new Terminal();
        this.terminal.open(document.getElementById('terminal'));
        this.terminal.write('Give me a task: ');

        // Create an instance of the Input class
        const inputHandler = new Input();

        // Listen for input events
        this.terminal.onData((input) => {

            const output = inputHandler.handler(input);
            this.terminal.write(output);
        });
    }

    render() {
        return (
            <div className="App">
                <div id="terminal"></div>
            </div>
        );
    }
}

// Render the App component to the root element
ReactDOM.render(<App />, document.getElementById('root'));

export default App;
