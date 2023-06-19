import React from 'react';
import { render, screen } from '@testing-library/react';
import LandingPageBannerTextButton from '.'

describe('test LandingPageBannerTextButton component',()=>{
    it('renders LandingPageBannerTextButton correctly',()=>{
        const btn = {color:'#333', text:'button', url:'http://localhost.com'}
        render(<LandingPageBannerTextButton btn={btn}/>);
        const button = screen.getByTestId('banner-btn')
        expect(button).toBeInTheDocument()
        expect(button).toHaveStyle(`backgroundColor:#333`)
        expect(button).toHaveAttribute("href","http://localhost.com")
    })
})