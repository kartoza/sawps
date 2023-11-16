import React from 'react';
import './index.scss';
import LandingPageBanner from '../../components/LandingPage/LandingPageBanner';
import Footer from '../../components/Footer'
const isLoggedIn = (window as any).isLoggedIn;
import LandingPagePopulationOverview from '../../../src/components/LandingPage/LandingPagePopulationOverview'

function HomePage() {
  return (
    <div className="App LandingPage">
      <LandingPageBanner/>
      <LandingPagePopulationOverview/>
      <Footer/>
    </div>
  );
}

export default HomePage;
