import React from 'react';
import { createRoot } from "react-dom/client";
import './assets/styles/index.scss';
import reportWebVitals from './reportWebVitals';
import HomePage from './containers/HomePage';
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from '@mui/material/styles';
import theme from './utils/Theme';

const rootElement = document.getElementById('app')!
const root = createRoot(rootElement);

root.render(
    <ErrorBoundary>
        <ThemeProvider theme={theme}>
            <HomePage/>
        </ThemeProvider>
    </ErrorBoundary>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
