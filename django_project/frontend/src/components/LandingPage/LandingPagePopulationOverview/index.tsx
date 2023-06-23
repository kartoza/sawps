import React, { FC } from 'react';
import './styles.scss'
import LandingPagePopulationOverviewHeader from './LandingPagePopulationOverviewHeader';
import OverviewCardsHolder from './OverviewCardsHolder';

interface ILandingPagePopulationOverview {}


const LandingPagePopulationOverview:FC<ILandingPagePopulationOverview>=()=>{
    return(
        <>
            <div className='landing-page-population-overview-container' data-testid="landing-page-population-overview-container">
                <LandingPagePopulationOverviewHeader />
                <OverviewCardsHolder />
            </div>
        </>
    )
}


export default LandingPagePopulationOverview;