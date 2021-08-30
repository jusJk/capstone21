import React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Box from '@material-ui/core/Box';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';


import { createTheme } from '@material-ui/core/styles';

const theme = createTheme({
  palette: {
    primary: {
      light: '#e5ffff',
      main: '#eceff1  ',
      dark: '#82ada9',
      contrastText: '#34515e',
    },
    secondary: {
      light: '#ff7961',
      main: '#f44336',
      dark: '#ba000d',
      contrastText: '#000',
    },
    typography:{
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
      ].join(','),
    }
  },
});
export default function Nav() {
  return(
  <div>
    <Box sx={{ flexGrow: 1 }}>
      <ThemeProvider theme={theme}>
      <AppBar position="static" >
        <Toolbar>
          <IconButton
            size="xlarge"
           

            aria-label="menu"
            sx={{ mr: 2 }}
          >
            
          
           <img style={{ maxWidth: "20vh" }} alt='' src="engineering.png"></img>
            
           
            
            
          </IconButton>
          <Typography variant="h5" component="div" sx={{ flexGrow: 1 }}>
            <b >AI AS A SERVICE</b>
            
          </Typography>
         
        </Toolbar>
      </AppBar>

      </ThemeProvider>
      
    </Box>
    </div>
  );
}
