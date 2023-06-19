import React, {FC} from 'react';
import './index.scss';

interface IContact {}

const Contact:FC<IContact>=()=>{
    return(
        <>
            <div className='contact-container' data-testid='contact-container'>
                <div className='contact-content-container'>
                    <div className='contact-image-container'>
                        <div className='contact-banner-img'></div>
                    </div>
                    <div className='contact-texts-container'>
                        <div className='contact-texts-inner-container'>
                            <div className='contact-content-title'>
                                Contact Us
                            </div>
                            <div className='contact-form-container'>
                                <div className='contact-form'>
                                <form>
                                    <div className='contact-form-input-name'>
                                        <label htmlFor="contact-name">Name</label><br/>
                                        <input id='contact-name' name="Name" type='text'/>
                                    </div>

                                    <div className='contact-form-input-email'>
                                        <label htmlFor="contact-name">Email</label><br/>
                                        <input id='contact-email' name="Email" type='text'/>
                                    </div>

                                    <div className='contact-form-inputs-subject'>
                                        <label htmlFor="contact-name">Subject</label><br/>
                                        <input id='contact-subject' name="Subject" type='text'/>
                                    </div>

                                    <div className='contact-form-inputs-message'>
                                        <label htmlFor="contact-name">Message</label><br/>
                                        <input id='contact-message' name="Message" type='textarea'/>
                                    </div>

                                </form>
                                </div>
                            </div>
                            <div className='contact-btns-container'>
                                <div className='contact-checkbox-container'>
                                    <input type="checkbox" name="checkbox"/>
                                    <label className="contact-send-email">Send me a copy</label>
                                </div>
                                <a href="#" className='contact-anchor'>SEND</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Contact