import React, { useState } from 'react';
import TerminalLib from './input-handler';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';
import './styles.css';
import HostManager from './HostManager';
import { CssBaseline, Container, AppBar, Toolbar, Typography, IconButton, Drawer } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';


function App() {
    const [drawerOpen, setDrawerOpen] = useState(false);
    const terminalHandler = new TerminalLib();
    const darkTheme = createTheme({
        palette: {
            type: 'dark',
        },
    });

    React.useEffect(() => {
        // Initialize the terminal
        terminalHandler.init();
    }, []);

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }
        setDrawerOpen(open);
    };

    return (
        <ThemeProvider theme={darkTheme}>
        <div className="App">
        <CssBaseline />
        <AppBar position="static">
            <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu" onClick={toggleDrawer(true)}>
                <MenuIcon />
            </IconButton>
            <Typography variant="h6">
                GPT SysAdmin
            </Typography>
            </Toolbar>
        </AppBar>
        <Container>
            <div id="terminal"></div>
        </Container>
        <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
            <div role="presentation">
            <HostManager />
            </div>
        </Drawer>
        </div>
        </ThemeProvider>
    );
}

export default App;
