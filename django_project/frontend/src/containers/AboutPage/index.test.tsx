import React from 'react';
import { render, screen } from '@testing-library/react';
import About from './About';

describe('testing About page',()=>{
    it('renders About page',()=>{
        render(<About/>)
        const AboutContainer = screen.getByTestId('about-page-container')
        expect(AboutContainer).toBeInTheDocument()

        const AboutPageTitle = 'The Wild life Population system'
        const AboutTitle = screen.getByText(AboutPageTitle)
        expect(AboutTitle).toBeInTheDocument()

        const VideoFrame = screen.getByTestId('about-page-video-frame')
        expect(VideoFrame).toBeInTheDocument()
        expect(VideoFrame).toHaveAttribute("src","https://www.youtube.com/embed/iM2fkxVmq9w")
    })
})