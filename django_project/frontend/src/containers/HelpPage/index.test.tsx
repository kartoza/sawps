import React from 'react'
import { render, screen } from '@testing-library/react';
import Help from './Help'


describe('testing Help page component',()=>{
    it('renders Help component',()=>{
        render(<Help/>)
        const helpContainer = screen.getByTestId('help-container')
        expect(helpContainer).toBeInTheDocument()
        const helpSectionTitle = screen.getByText('Help & Support')
        expect(helpSectionTitle).toBeInTheDocument()

        const userGuideAnchor = screen.getByTestId('user-guide-anchor')
        expect(userGuideAnchor).toHaveAttribute("href","/user_guide")

        const Contact = screen.getByTestId('contact-anchor')
        expect(Contact).toHaveAttribute("href","/contact")
    })
})