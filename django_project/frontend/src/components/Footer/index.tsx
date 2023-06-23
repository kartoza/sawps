import React, { FC } from 'react';
import './index.scss';

interface IFooter{}


const Footer:FC<IFooter>=()=>{
    return (
      <div className='footer'>
          {/* Made with <img className='heart' src='/static/images/heart-icon.png'/> by&nbsp; 
          <a href='https://kartoza.com' target='_blank' style={{ color: "var(--white)"}}>Kartoza</a> */}
            <div className='sanbi-footer-logo-container'>
                <img className='footer-logo' src='/static/images/footer/footer-logo.png'/>
            </div>
            <div className='footer-nav'>
                <a href='/' target='_blank'>HOME</a>
                <a href='/map' target='_blank'>MAP</a>
                <a href='/documentation' target='_blank'>DOCUMENTATION</a>
                <a href='/contact' target='_blank'>CONTACT</a>
          </div>
          <div className='vendors-logos-container'>
            <img className='ids-logo' src='/static/images/footer/ids-logo.png'/>
            <img className='kartoza-white-logo' src='/static/images/footer/kartoza-white.png'/>
          </div>
      </div>
    );
  }
  

  export default Footer