import React from 'react';
import './index.scss';
import { Box, Button, Grid, Paper, Typography } from '@mui/material';
import LandingPagePopulationOverview from '../../components/LandingPage/LandingPagePopulationOverview';
import CustomButton from '../../components/Button';
import LandingPageBanner from '../../components/LandingPage/LandingPageBanner';
import Footer from '../../components/Footer'


const isLoggedIn = (window as any).isLoggedIn;




function HomePage() {
  return (
    <div className="App">
      <LandingPageBanner/>
      <LandingPagePopulationOverview/>
      <Footer/>
    </div>
  );
}

export default HomePage;
