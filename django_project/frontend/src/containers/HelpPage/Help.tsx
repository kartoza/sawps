import React, { FC } from 'react';
import { HelperContainer } from "../../components/HelperContainer";

import './index.scss';

import "django-docs-crawler-react/dist/style.css"

interface IHelp {
}

const Help: FC<IHelp> = () => {
  return (
    <>
      <div className='help-container' data-testid='help-container'>
        <div className='help-content-container'>
          <div className='help-image-container'>
            <img src='/static/images/help/help_page_banner.png'
                 className="help-banner-img" alt="Help Banner"/>
          </div>
          <div className='help-texts-container'>
            <HelperContainer
              relativeUrl='/help/'
              open={true}
              setOpen={() => {
              }}
              footer={
                <div className='help-btns-container'>
                  <a href="/contact">
                    <button
                      className="orange-button sawps-font-button-black">
                      Contact us
                    </button>
                  </a>
                </div>
              }
            />
          </div>
        </div>
      </div>
    </>
  )
}

export default Help