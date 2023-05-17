import React from 'react';
import ResponsiveNavbar from '../../components/Navbar';
import './index.scss';
import { Box, Button, Grid, Paper, Typography } from '@mui/material';

function Banner() {
  return (
    <Paper
      sx={{
        color: '#fff',
        height: { xs: 500, md: 800 },
        maxWidth: '100%',
        backgroundImage: `url(/static/images/lion.png)`,
        backgroundSize: { xs: '70%', md: 'auto 100%' },
        backgroundPosition: 'left',
        backgroundRepeat: 'no-repeat',
        backgroundColor: '#000',
        borderRadius: 0
      }}
    >
      <Grid container spacing={1} sx={{ height: '100%' }}>
        <Grid item xs={2} md={7} xl={6}></Grid>
        <Grid item xs={4}>
          <Box className='banner-description'>
            <Typography variant="h3" component="h3" gutterBottom>
              Wild life population system monitoring traded wildlife in South Africa
            </Typography>
            <Box className='banner-button-container'>
              <Button title='About'>About</Button>
              <Button title='About'>Explore</Button>
            </Box>
          </Box>
        </Grid>
      </Grid>
      
    </Paper>
  );
}


function HomePage() {
  return (
    <div className="App">
      <ResponsiveNavbar/>
      <Banner/>
    </div>
  );
}

export default HomePage;
