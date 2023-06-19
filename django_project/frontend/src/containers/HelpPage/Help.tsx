import React, { FC } from 'react';
import './index.scss';

interface IHelp{}

const Help:FC<IHelp> = ()=>{
    return(
        <>
            <div className='help-container' data-testid='help-container'>
                <div className='help-content-container'>
                    <div className='help-image-container'>
                        <div className='help-banner-img'></div>
                    </div>
                    <div className='help-texts-container'>
                        <div className='help-content-title'>
                            Help & Support
                        </div>
                        <div className='help-text-container'>
                            <div className='help-text'>
                            the WLPS platform offers a broad range of features which are documented in a full user guide. 
                            For any other queries please contact the site administration using the contact from.
                            </div>
                        </div>
                        <div className='help-btns-container'>
                            <a href="/user_guide" className='user-guide-anchor' data-testid='user-guide-anchor'>User guide</a>
                            <a href="/contact" className='contact-anchor' data-testid='contact-anchor'>Contact us</a>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Help