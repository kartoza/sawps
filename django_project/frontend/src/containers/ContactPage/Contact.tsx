import React, {FC} from 'react';
import './index.scss';

interface IContact {}

const Contact:FC<IContact>=()=>{
    return(
        <>
            <div className='contact-container' data-testid='contact-container'>
                <div className='contact-content-container'>
                    <div className='col-12 row mr-0 ml-0'>
                        <div className='col-lg-7 col-md-2 d-none d-sm-block contact-image-container'>
                            <div className='contact-banner-img'></div>
                        </div>
                        <div className='col-lg-4 col-md-9 col-xs-12 contact-texts-container '>
                            <div className='contact-texts-inner-container pt-4 pb-3'>
                                <div className='contact-content-title'>
                                    <h3>Contact Us</h3>
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
                                            <textarea id='contact-message' name="Message"/>
                                        </div>

                                    </form>
                                    </div>
                                </div>
                                <div className='contact-btns-container container'>
                                    <div className="row col-12">
                                        <div className='col-md-2  d-none d-sm-block'></div>
                                        <div className='col-xs-12 col-md-4 pb-2 contact-checkbox-container'>
                                            <input type="checkbox" name="checkbox" id="sendCopy"/>
                                            <label htmlFor="sendCopy" className="contact-send-email">Send me a copy</label>
                                        </div>
                                        <div className="col-xs-12 col-md-3 d-flex justify-content-center">
                                            <a href="#" className='contact-anchor'>SEND</a>
                                        </div>
                                        <div className='col-md-3  d-none d-sm-block'></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className='col-lg-1  d-none d-md-block'></div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Contact