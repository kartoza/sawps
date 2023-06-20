import React from 'react'
import {render, screen} from '@testing-library/react'
import Contact from './Contact'

describe("testing contact component",()=>{
    it("test rendering contact component",()=>{
        render(<Contact/>)
        const contactContainer = screen.getByTestId('contact-container')
        expect(contactContainer).toBeInTheDocument()

        const contactTitle = screen.getByText('Contact Us')
        expect(contactTitle).toBeInTheDocument()

        const contactName = screen.getByText('Name')
        expect(contactName).toBeInTheDocument()

        const contactEmail = screen.getByText('Email')
        expect(contactEmail).toBeInTheDocument()


        const contactSubject = screen.getByText('Subject')
        expect(contactSubject).toBeInTheDocument()

        const contactMessage = screen.getByText('Message')
        expect(contactMessage).toBeInTheDocument()

        const sendCopyCheckbox = screen.getByText('Send me a copy')
        expect(sendCopyCheckbox).toBeInTheDocument()


        const sendButton = screen.getByText('SEND')
        expect(sendButton).toBeInTheDocument()
        expect(sendButton).toHaveAttribute('href','#')
    })
})