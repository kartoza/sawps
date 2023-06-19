import React from 'react';
import { render, screen } from '@testing-library/react';

import LandingPageBanner from '.'

describe("testing landing page banner",()=>{
    it("render LandingPageBanner correctly",()=>{
        render(<LandingPageBanner/>)
        const cardsHolderContainer = screen.getByTestId("landing-page-banner")
        expect(cardsHolderContainer).toBeInTheDocument()
    })
})
