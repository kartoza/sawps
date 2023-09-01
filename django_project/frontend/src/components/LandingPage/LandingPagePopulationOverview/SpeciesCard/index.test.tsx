import React from 'react';
import { render, screen } from '@testing-library/react';
import SpeciesCard from '.';
//

describe('species card testing suite', ()=>{
    it('renders species card component',()=>{
        render(<SpeciesCard species_id={1} pic='http://images.google.com' population='300' total_area={200} chartColors={{"line":"fff","area":"fff"}}/>)
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

        const speciesPopulationGrowthText = screen.getByTestId('species-card-total-area')
        expect(speciesPopulationGrowthText).toBeInTheDocument()
        expect(speciesPopulationGrowthText).toContain(200)        
    })
})