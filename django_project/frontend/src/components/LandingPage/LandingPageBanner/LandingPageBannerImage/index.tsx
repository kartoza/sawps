import React, { FC } from 'react';
import './styles.scss'

interface ILandingPageBannerImage{}


const LandingPageBannerImage:FC<ILandingPageBannerImage> = ()=> {
    return (
        <>
            <div className="landing-page-banner-image-container">
                <div className='landing-page-banner-image-inner-container'>
                    <div className='landing-page-banner-image' data-testid='landing-page-banner-image'></div>
                </div>
            </div>
        </>
    )
}


export default LandingPageBannerImage