import React from 'react';
import { render, screen } from '@testing-library/react';

import LandingPagePopulationOverviewHeader from '.'

describe("testing landing page overview header component",()=>{
    it("renders landing page header correctly",()=>{
        render(<LandingPagePopulationOverviewHeader/>)
        const cardsHolderContainer = screen.getByTestId("landing-page-population-overview-header")
        expect(cardsHolderContainer).toBeInTheDocument()

        const HeaderText = screen.getByText('SPECIES POPULATION OVERVIEW')
        expect(cardsHolderContainer).toBeInTheDocument()

        const HeaderSeparator = screen.getByTestId("landing-page-header-separator")
        expect(HeaderSeparator).toBeInTheDocument()
        

    })
})