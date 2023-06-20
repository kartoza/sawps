import React from 'react';
import { createRoot } from "react-dom/client";
import { Provider } from 'react-redux';
import { store } from '../../app/store';
import './index.scss';
import reportWebVitals from '../../reportWebVitals';
import About from './About';
import ErrorBoundary from "../../components/ErrorBoundary";
import theme from '../../utils/Theme';
import { ThemeProvider } from '@mui/material';


const rootElement = document.getElementById('app')!
const root = createRoot(rootElement);

root.render(
    <Provider store={store}>
        <ErrorBoundary>
            <ThemeProvider theme={theme}>
                <About/>
            </ThemeProvider>
        </ErrorBoundary>
    </Provider>
);