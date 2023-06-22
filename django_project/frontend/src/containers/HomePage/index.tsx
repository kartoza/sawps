import React from 'react';
import './index.scss';
import { Box, Button, Grid, Paper, Typography } from '@mui/material';
import LandingPagePopulationOverview from '../../components/LandingPage/LandingPagePopulationOverview';
import CustomButton from '../../components/Button';
import LandingPageBanner from '../../components/LandingPage/LandingPageBanner';

const isLoggedIn = (window as any).isLoggedIn;


function Footer() {
  return (
    <div className='footer'>
        Made with <img className='heart' src='/static/images/heart-icon.png'/> by&nbsp; 
        <a href='https://kartoza.com' target='_blank' style={{ color: "var(--white)"}}>Kartoza</a>
    </div>
  );
}


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
