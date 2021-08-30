import React from "react";
import { useState } from "react";
import Drawer from "@material-ui/core/Drawer";
import { makeStyles } from "@material-ui/core/styles";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import ListItem from "@material-ui/core/ListItem";
import InboxIcon from "@material-ui/icons/MoveToInbox";
import MailIcon from "@material-ui/icons/Mail";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import { withStyles } from "@material-ui/core/styles";
import MuiAccordion from "@material-ui/core/Accordion";
import MuiAccordionSummary from "@material-ui/core/AccordionSummary";
import MuiAccordionDetails from "@material-ui/core/AccordionDetails";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import CollectionsBookmarkIcon from "@material-ui/icons/CollectionsBookmark";
import InfoIcon from "@material-ui/icons/Info";


const drawerWidth = 240;
const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },

  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    zIndex: 1,
    textAlign: "left",
  },
  drawerPaper: {
    width: drawerWidth,
  },
  h3: {
    marginLeft: "5%",
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(3),
  },
  nested: {
    paddingLeft: theme.spacing(4),
  },
}));

const Accordion = withStyles({
  root: {
    border: "0px solid rgba(0, 0, 0, .125)",
    boxShadow: "none",

    borderBottom: 0,

    "&:before": {
      display: "none",
    },
    "&$expanded": {
      margin: "0",
     
    },
  },
  expanded: {},
})(MuiAccordion);

const AccordionSummary = withStyles({
  root: {
    backgroundColor: "",
    marginBottom: -1,
    minHeight: 56,
    "&$expanded": {
      minHeight: 56,
    },
  },
  content: {
    "&$expanded": {
      margin: "12px 0",
    },
  },
  expanded: {},
})(MuiAccordionSummary);

const AccordionDetails = withStyles((theme) => ({
  root: {
    padding: 0,
    paddingLeft: theme.spacing(4),

  },
}))(MuiAccordionDetails);

export default function SideBar(props) {
   
  const classes = useStyles();


  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
      anchor="left"
    >
      <div className={classes.toolbar} />
      <Divider />
      <h3 className={classes.h3}>Menu</h3>
      <Divider />
     
    

      {["LPD-Net", "Body-Pose Estimation", "Model 3", "Model 4"].map((text, index)=>(
          <Accordion>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1a-content"
            id="panel1a-header"
          >
            <ListItem>
              <ListItemIcon>
                <CollectionsBookmarkIcon></CollectionsBookmarkIcon>
              </ListItemIcon>
              <ListItemText>{text} </ListItemText>
            </ListItem>
          </AccordionSummary>
          <AccordionDetails>
            <List>
              {["Model Demo", "Model Info", "Model Drift"].map(
                (text, index) => (
                  <ListItem button key={text} >
                    <ListItemIcon>
                      {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                    </ListItemIcon>
                    <ListItemText primary={text} />
                  </ListItem>
                 
                )
              )}
            </List>
            <Divider/>
          </AccordionDetails>
        </Accordion>

      )

      )}
      
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel2a-content"
          id="panel2a-header"
        >
          <ListItem>
            <ListItemIcon>
              <InfoIcon />
            </ListItemIcon>
            <ListItemText>About</ListItemText>
          </ListItem>
        </AccordionSummary>
        <AccordionDetails>
          <List>
            {["Architecture", " Contact"].map((text, index) => (
              <ListItem button key={text}>
                <ListItemIcon>
                  {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </AccordionDetails>
      </Accordion>

      <Divider />
    </Drawer>
  );
}
