import TerminalLib from './input-handler';
import React from 'react';
import ReactDOM from 'react-dom';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';
import './styles.css';

class App extends React.Component {
    componentDidMount() {
        // Initialize the terminal
        const terminalHandler = new TerminalLib();
        terminalHandler.init();
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
