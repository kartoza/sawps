import React from 'react';
import ResponsiveNavbar from '../../components/Navbar';
import './index.scss';
import { Container, Box, Button, Grid, Paper, Typography } from '@mui/material';

const csrf_token = (window as any).csrfToken;


function Form(){
    return (
        <Container maxWidth="sm">
            
        </Container>

    );
}

function LoginPage() {
    return (
      <div className="App">
        <ResponsiveNavbar/>
        <Form/>
      </div>
    );
  }

  export default LoginPage