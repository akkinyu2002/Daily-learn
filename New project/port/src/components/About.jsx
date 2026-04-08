import React from 'react';
import './About.css';

const About = () => {
    return (
        <section id="about" className="about">
            <div className="container">
                <h2 className="section-title"><span>01.</span> About Me</h2>

                <div className="about-content">
                    <div className="about-text glass">
                        <p>
                            I am a creative and adaptable individual with skills in graphic design, video editing, and content creation.
                            With a background in IT and a Diploma in Computer Engineering, I am passionate about technology,
                            cybersecurity, and innovative digital media projects. I have a strong ability to learn quickly and work independently.
                        </p>
                    </div>

                    <div className="timeline-section">
                        <h3 className="timeline-title">Experience</h3>
                        <div className="timeline-item">
                            <div className="timeline-dot"></div>
                            <div className="timeline-content glass">
                                <h4>Voluntary Teacher</h4>
                                <span className="timeline-date">Oct 2023 - Jan 2024</span>
                                <p className="timeline-company">Shree Saraswati Secondary School</p>
                                <p>Intermediate educator skilled in lesson planning, student engagement, and fostering a positive learning environment.</p>
                            </div>
                        </div>
                        <div className="timeline-item">
                            <div className="timeline-dot"></div>
                            <div className="timeline-content glass">
                                <h4>OJT (On the Job Training)</h4>
                                <span className="timeline-date">Sep 2021 - Dec 2023</span>
                                <p className="timeline-company">Panil Tech / Saraswati Secondary School</p>
                                <p>12 months of OJT in multiple phases. Gained hands-on experience in front-end development, C# Windows application development, and mobile application development.</p>
                            </div>
                        </div>
                    </div>

                    <div className="timeline-section">
                        <h3 className="timeline-title">Education</h3>
                        <div className="timeline-item">
                            <div className="timeline-dot"></div>
                            <div className="timeline-content glass">
                                <h4>Diploma in Computer Engineering (SLC)</h4>
                                <span className="timeline-date">Sep 2021 - Jul 2023</span>
                                <p className="timeline-company">Shree Saraswati Secondary School</p>
                                <p>GPA: 3.39</p>
                            </div>
                        </div>
                        <div className="timeline-item">
                            <div className="timeline-dot"></div>
                            <div className="timeline-content glass">
                                <h4>SEE (School Education Examination)</h4>
                                <span className="timeline-date">Apr 2017 - Jul 2021</span>
                                <p className="timeline-company">Shree Saraswati Secondary School</p>
                                <p>GPA: 3.84 (IT Stream)</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default About;
