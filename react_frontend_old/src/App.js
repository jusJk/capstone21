import React from "react";
import "./App.css";
import Nav from "./Dashboard/Nav";
import Dash from "./Dashboard/Dash";

// routes
import Router from './routes';
// theme
import ThemeConfig from './theme/index.js';
// components
import ScrollToTop from './components/ScrollToTop.js';

// ----------------------------------------------------------------------

export default function App() {
  return (
    <ThemeConfig>
      <ScrollToTop />
      <Router />
    </ThemeConfig>
  );
}


// import { ThemeProvider } from '@material-ui/core/styles';
// import { createTheme } from '@material-ui/core/styles';
// function App() {
//   const theme = createTheme({
//     palette: {
//       primary: {
//         light: "#e5ffff",
//         main: "#eceff1",
//         dark: "#82ada9",
//         contrastText: "#34515e",
//       },
//       secondary: {
//         light: "#ff7961",
//         main: "#f44336",
//         dark: "#ba000d",
//         contrastText: "#000",
//       },
//       typography: {
//         fontWeight: "bold",
//         fontFamily: [
//           "-apple-system",
//           "BlinkMacSystemFont",
//           '"Segoe UI"',
//           "Roboto",
//           '"Helvetica Neue"',
//           "Arial",
//           "sans-serif",
//           '"Apple Color Emoji"',
//           '"Segoe UI Emoji"',
//           '"Segoe UI Symbol"',
//         ].join(","),
//       },
//     },
//   });
//   return (
//     <div className="App">
//       <ThemeProvider theme={theme}>
//         <Nav></Nav>
//         <Dash></Dash>
//       </ThemeProvider>

//       {/* <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
          
//         </a>
//       </header> */}
//     </div>
//   );
// }

// export default App;
