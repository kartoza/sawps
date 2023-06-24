import React, { FC } from 'react';
import './styles.scss'

interface ILandingPagePopulationOverviewHeader{}

const LandingPagePopulationOverviewHeader:FC<ILandingPagePopulationOverviewHeader> = ()=>{
    return(
        <>
            <div className='landing-page-population-overview-header' data-testid="landing-page-population-overview-header">
                <p>NATIONAL POPULATION OVERVIEW</p>
                <hr className='landing-page-population-overview-header-separator' data-testid="landing-page-header-separator"/>
            </div>
        </>
    )
}

export default LandingPagePopulationOverviewHeader