import React from 'react'
import {render, screen} from '@testing-library/react'
import Footer from './index'

describe("testing contact component",()=>{
    it("test rendering contact component",()=>{
        render(<Footer/>)
        const footerContainer = screen.getByTestId('footer')
        expect(footerContainer).toBeInTheDocument()

        const sanbiFooterLogo = screen.getByTestId('sanbi-footer-logo')
        expect(sanbiFooterLogo).toBeInTheDocument()
        expect(sanbiFooterLogo).toHaveAttribute("src","/static/images/footer/footer-logo.png")

        const footerNavigation = screen.getByTestId('footer-navigation')
        expect(footerNavigation).toBeInTheDocument()

        const FooterNavigationHome = screen.getByText('HOME')
        expect(FooterNavigationHome).toBeInTheDocument()
        expect(FooterNavigationHome).toHaveAttribute("href","/")

        const FooterNavigationMap = screen.getByText('MAP')
        expect(FooterNavigationMap).toBeInTheDocument()
        expect(FooterNavigationMap).toHaveAttribute("href","/map")

        const FooterNavigationDocumentation = screen.getByText('DOCUMENTATION')
        expect(FooterNavigationDocumentation).toBeInTheDocument()
        expect(FooterNavigationDocumentation).toHaveAttribute("href","/")

        const FooterNavigationContact = screen.getByText('CONTACT')
        expect(FooterNavigationContact).toBeInTheDocument()
        expect(FooterNavigationContact).toHaveAttribute("href",'/contact')

        const vendorsLogosContainer = screen.getByTestId('vendors-logos-container')
        expect(vendorsLogosContainer).toBeInTheDocument()

        const IDSLogo = screen.getByTestId('ids-logo')
        expect(IDSLogo).toBeInTheDocument()

        const KartozaLogo = screen.getByTestId('kartoza-logo')
        expect(KartozaLogo).toBeInTheDocument()



    })
})