import React from 'react';
import { render, screen } from '@testing-library/react';
import SpeciesCard from '.';
//

describe('species card testing suite', ()=>{
    it('renders species card component',()=>{
        render(<SpeciesCard pic='http://images.google.com' population='300' growth='200' loss='100' chartColors={{"line":"fff","area":"fff"}}/>)
        const speciesCard = screen.getByTestId('species-card-container')
        expect(speciesCard).toBeInTheDocument()
    })

    it('correctly renders props',()=>{
        const speciesImage = screen.getByTestId('species-card-image')
        expect(speciesImage).toBeInTheDocument()
        expect(speciesImage).toHaveAttribute("src","http://images.google.com")
        
        const speciesTotalPopulationText = screen.getByTestId('species-card-population')
        expect(speciesTotalPopulationText).toBeInTheDocument()
        expect(speciesTotalPopulationText).toContain("300")

        const speciesPopulationGrowthText = screen.getByTestId('species-card-growth')
        expect(speciesPopulationGrowthText).toBeInTheDocument()
        expect(speciesPopulationGrowthText).toContain("200")


        const speciesPopulationLossText = screen.getByTestId('species-card-loss')
        expect(speciesPopulationLossText).toBeInTheDocument()
        expect(speciesPopulationLossText).toContain("200")
        
        
    })
})