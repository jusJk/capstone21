import React from 'react';

import AppBar from '@material-ui/core/AppBar';
import Box from '@material-ui/core/Box';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import {makeStyles} from '@material-ui/core'



const useStyles = makeStyles((theme) => ({
  appBar: {
    position: 'relative',
    zIndex: 1400,
},
}))

export default function Nav() {
  const  classes = useStyles();

  return(
  <div>
    <Box sx={{ flexGrow: 1 }}>
     
      <AppBar  className={classes.appBar}>
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

      
      
    </Box>
    </div>
  );
}
