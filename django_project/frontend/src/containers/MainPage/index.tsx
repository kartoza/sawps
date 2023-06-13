import React from 'react';
import { createRoot } from "react-dom/client";
import { Provider } from 'react-redux';
import { store } from '../../app/store';
import './index.scss';
import reportWebVitals from '../../reportWebVitals';
import MainPage from '../MainPage/MainPage';
import ErrorBoundary from "../../components/ErrorBoundary";
import theme from '../../utils/Theme';
import { ThemeProvider } from '@mui/material';


const rootElement = document.getElementById('app')!
const root = createRoot(rootElement);

root.render(
    <Provider store={store}>
        <ErrorBoundary>
            <ThemeProvider theme={theme}>
                <MainPage/>
            </ThemeProvider>
        </ErrorBoundary>
    </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
