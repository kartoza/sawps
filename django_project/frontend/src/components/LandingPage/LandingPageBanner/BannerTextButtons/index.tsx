import React, { FC } from 'react';
import './styles.scss'

interface IBtn{
    color:string,
    text:string,
    url:string
}

interface IBannerTextButtonProps{
    btn:IBtn 
}

const LandingPageBannerTextButton:FC<IBannerTextButtonProps> = (props)=>{
    return(
        <>
            <a className="landing-page-banner-btn" style={{backgroundColor:props.btn.color}}
                href={props.btn.url}
                data-testid='banner-btn'
            >
                {props.btn.text}
            </a>
        </>
    )
}

export default LandingPageBannerTextButton