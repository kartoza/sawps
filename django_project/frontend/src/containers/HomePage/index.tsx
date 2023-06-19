import React from 'react';
import ResponsiveNavbar from '../../components/Navbar';
import './index.scss';
import { Box, Button, Grid, Paper, Typography } from '@mui/material';
<<<<<<< HEAD
import LandingPageBanner from '../../components/LandingPage/LandingPageBanner';
import LandingPagePopulationOverview from '../../components/LandingPage/LandingPagePopulationOverview';


=======
import CustomButton from '../../components/Button';

const isLoggedIn = (window as any).isLoggedIn;
>>>>>>> d9838092f283ec62aa7e43ee7db437a7dfe2578b

function Banner() {
  return (
    <Paper
      sx={{
        color: '#fff',
        height: { xs: 500, md: 800 },
        maxWidth: '100%',
        backgroundImage: `url(/static/images/not-lion.png)`,
        backgroundSize: { xs: '70%', md: 'auto 90%' },
        backgroundPosition: 'left',
        backgroundRepeat: 'no-repeat',
        backgroundColor: '#000',
        borderRadius: 0
      }}
    >
      <Grid container spacing={1} sx={{ height: '100%' }}>
        <Grid item xs={1} md={6} xl={5}></Grid>
        <Grid item xs={5}>
          <Box className='banner-description'>
            <Typography variant="h3" component="h3" gutterBottom>
              Wild life population system monitoring traded wildlife in South Africa
            </Typography>
            <Box className='banner-button-container'>
              <CustomButton color='green' title='About'>About</CustomButton>
              {isLoggedIn ? <>
                <CustomButton color='orange' title='About' onClick={() => window.location.href = '/map'}>Explore</CustomButton>
                <CustomButton color='purple' title='About'>Upload Your Data</CustomButton>
              </> : <>
                <CustomButton color='orange' title='About' onClick={() => window.location.href = '/accounts/login/'}>Login</CustomButton>
                <CustomButton color='purple' title='About' onClick={() => window.location.href = '/accounts/signup/'}>Register</CustomButton>
              </>}
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
      {/* <Banner/> */}
      <LandingPageBanner />
      <LandingPagePopulationOverview/>  
    </div>
  );
}

export default HomePage;
