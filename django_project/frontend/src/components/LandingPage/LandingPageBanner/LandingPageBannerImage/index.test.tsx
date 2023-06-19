import React from 'react';
import { render, screen } from '@testing-library/react';

import LandingPageBannerImage from '.'

describe("testing landing page banner image",()=>{
    it("renders LandingPageBannerImage correctly",()=>{
        render(<LandingPageBannerImage/>)
        const BannerImage = screen.getByTestId("landing-page-banner-image")
        expect(BannerImage).toBeInTheDocument()
    })
})
