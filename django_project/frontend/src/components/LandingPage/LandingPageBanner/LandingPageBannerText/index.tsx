import React, { FC } from 'react';
import './styles.scss'
import CustomButton, { ButtonColor } from '../../../Button';


interface ILandingPageBannerImage{}

const LandingPageBannerText:FC<ILandingPageBannerImage> =() =>{
    const btnProps = [
        {"text":"About", "color":"green","url":"/about"},
        {"text":"Login", "color":"orange","url":"/accounts/login/"},
        {"text":"Register","color":"purple","url":"/accounts/signup/"}
    ]
    return (
        <>
            <div className="landing-page-banner-text-container">
                <div className='landing-page-banner-text-header-container'>
                    <div className='landing-page-banner-text-header'>
                        SOUTH AFRICAN WILDLIFE POPULATION SYSTEM
                        MONITORING TRADED WILDLIFE IN SOUTH AFRICA
                    </div>
                </div>
                <div className='landing-page-banner-text-btns-container'>
                    {
                        btnProps.map((prop, index) => 
                            <div className='landing-page-banner-text-btns' key={index}>
                                <CustomButton onClick={() => window.location.href = prop.url} color={prop.color as ButtonColor} buttonText={prop.text} sx={{ width: 150, mr: 2 }} />
                            </div>
                        )
                    }
                </div>
                <div className="landing-page-banner-text-paragraph">
                    <p>Securely contribute, store, visualise and analyse species population data.
                        Automatically get species population reports for priority species on your properties.</p>
                </div>
            </div>
        </>
    )
}


export default LandingPageBannerText