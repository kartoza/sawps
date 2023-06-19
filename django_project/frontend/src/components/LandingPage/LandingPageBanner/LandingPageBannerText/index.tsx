import React, { FC } from 'react';
import './styles.scss'
import CustomButton from '../../../Button';


interface ILandingPageBannerImage{}

const LandingPageBannerText:FC<ILandingPageBannerImage> =() =>{
    const btnProps = [
        {"text":"About", "color":"green","url":"/about"},{"text":"Login", "color":"orange","url":"/login"},{"text":"Register","color":"purple","url":"/register"}
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
                            if(prop.color=='green'){
                                return (
                                    <div className='landing-page-banner-text-btns' key={index}>
                                         <CustomButton color='green' buttonText={prop.text} sx={{width:150,mr:2}}/>
                                     </div>
                                 )

                            }

                            else if(prop.color=='orange'){
                                return (
                                    <div className='landing-page-banner-text-btns' key={index}>
                                         <CustomButton color='orange' buttonText={prop.text} sx={{width:150, mr:2}}/>
                                     </div>
                                 )
     
                            }

                            else{
                                return (
                                    <div className='landing-page-banner-text-btns' key={index}>
                                         <CustomButton color="purple" buttonText={prop.text} sx={{width:150,mr:2}}/>
                                     </div>
                                 )
     
                            }

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