import React, { FC } from 'react';
import './index.scss';

interface IAbout{}

const About:FC<IAbout> = ()=>{
    return(
        <>
            <section className='about-page fs-background' style={{ backgroundColor:'#000000'}}>
                <div className="container-fluid full-height position-absolute">
                <div className="row half-height about-container" data-testid='about-page-container'>
                    <div className='col-5'>
                    </div>
                    <div className='col-7'>
                        <div className='about-content-title'>
                                The Wild life Population system
                        </div>
                        <div className='about-subsection-1'>
                            <div className='about-subsection-1-video-holder'>
                            <iframe src="https://www.youtube.com/embed/iM2fkxVmq9w" title="Kruger National Park: Sightings from Northern Kruger" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowFullScreen data-testid='about-page-video-frame'></iframe> 
                            </div>
                            <div className='about-subsection-1-text'>
                                <p>The WLPS is a coordinated system of wildlife trade monitoring with centralised/shared information about priority species such as
                                rhino, lion, leopard, cheetah, elephant and more. See the Quick introduction video to get to know the platfrom
                                </p>
                            </div>
                        </div>
                        <div className='about-subsection-2'>
                            <h4>Securely Contribute and store your Species Data</h4>
                        </div>
                        <div className='about-subsection-3'>
                            <h4>Get automated data analysis and visualisation</h4>
                        </div>
                        <div className='about-subsection-4'>
                            <h4>Get automated data reports for submission to state bodies</h4>
                        </div>
                        <div className='about-subsection-5'>
                            <h4>use platform information and outputs for National Decision making</h4>
                        </div>
                    </div>
                </div>
                </div>
            </section>
        </>
    )
}


export default About
