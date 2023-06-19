import React, { FC } from 'react';
import './styles.scss'
import LandingPageBannerTextButton from '../BannerTextButtons'

interface ILandingPageBannerImage{}

const LandingPageBannerText:FC<ILandingPageBannerImage> =() =>{
    const btnProps = [
        {"text":"About", "color":"#70B276","url":"/about"},{"text":"Login", "color":"#FAA755","url":"/login"},{"text":"Register","color":"#9D85BE","url":"/register"}
    ]
    return (
        <>
            <div className="landing-page-banner-text-container">
                <div className='landing-page-banner-text-header-container'>
                    <b className='landing-page-banner-text-header'>Wild life Population system <br/> monitoring traded wildlife in south Africa</b>
                </div>
                <div className='landing-page-banner-text-btns-container'>
                    {
                        btnProps.map((prop, index) => {
                            return (
                               <div className='landing-page-banner-text-btns' key={index}>
                                    <LandingPageBannerTextButton btn={prop}/>
                                </div>
                            )
                        })
                    }
                </div>
                <div className="landing-page-banner-text-paragraph">
                    <h4>Securely contribute, store, visualise and analyse species population data.
                        Automatically get species population reports for <br className='landing-page-text-separator'/>priority species on your properties.</h4>
                </div>
            </div>
        </>
    )
}


export default LandingPageBannerText