import React, { FC } from 'react';
import './index.scss';

interface IAbout{}

const About:FC<IAbout> = ()=>{
    return(
        <>
            <div className='about-container' data-testid='about-page-container'>
                <div className='about-image-container'>
                    {/* <img src="about/about_page_main_img.png"/> */}
                </div>
                <div className='about-content-container'>
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
                    <div className='about-subsection-2'></div>
                    <div className='about-subsection-3'></div>
                    <div className='about-subsection-4'></div>
                    <div className='about-subsection-5'></div>
                </div>
            </div>
        </>
    )
}


export default About
