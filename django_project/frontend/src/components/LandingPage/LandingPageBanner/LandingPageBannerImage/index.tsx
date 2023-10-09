import React, { FC } from 'react';
import './styles.scss';

const LandingPageBannerImage: FC = () => {
  const backgroundImageStyle = {
    backgroundImage: `url('/static/images/species/rino_background.png')`,
    backgroundSize: 'contain',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    height: '100%',
    width: '100%',
    paddingLeft: '10%',
  };

  return (
    <div className="landing-page-banner-image-container">
      <div className='landing-page-banner-image-inner-container'>
        <div className='landing-page-banner-image' style={backgroundImageStyle} data-testid='landing-page-banner-image'></div>
      </div>
    </div>
  );
};

export default LandingPageBannerImage;
