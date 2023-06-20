import React, { FC } from 'react';
import './styles.scss'
import LandingPageBannerImage from './LandingPageBannerImage';
import LandingPageBannerText from './LandingPageBannerText'

interface ILandingPageBanner{}

const LandingPageBanner:FC<ILandingPageBanner> = () => {
    return (
        <>
            <div className="landing-page-banner" data-testid='landing-page-banner'>
                <LandingPageBannerImage/>
                <LandingPageBannerText/>
            </div>
        </>
    )
};

export default LandingPageBanner;