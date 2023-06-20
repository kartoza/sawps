import React from 'react';
import { render, screen } from '@testing-library/react';
import OverviewCardsHolder from '.'

describe("testing the cards holder component",()=>{
    it("renders card holder correctly",()=>{
        render(<OverviewCardsHolder/>)
        const cardsHolderContainer = screen.getByTestId("landing-page-overview-cards-holder")
        expect(cardsHolderContainer).toBeInTheDocument()
    })
})