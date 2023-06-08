import React from 'react';
import { createRoot } from "react-dom/client";
import { Provider } from 'react-redux';
import { store } from '../../app/store';
import './index.scss';
import reportWebVitals from '../../reportWebVitals';
import MainPage from '../MainPage/MainPage';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import ErrorBoundary from "../../components/ErrorBoundary";


const rootElement = document.getElementById('app')!
const root = createRoot(rootElement);
// to override MUI buttons theme
const { palette } = createTheme();
const { augmentColor } = palette;
const createColor = (mainColor: any) => augmentColor({
    color: {
        main: mainColor,
        contrastText: '#fff'
    }
});
const theme_override = createTheme({
    typography: {
        fontFamily: '"Poppins", sans-serif',
    },
  palette: {
    primary: createColor('#70B276')
  },
});

root.render(
    <Provider store={store}>
        <ErrorBoundary>
            <ThemeProvider theme={theme_override}>
                <MainPage/>
            </ThemeProvider>
        </ErrorBoundary>
    </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
