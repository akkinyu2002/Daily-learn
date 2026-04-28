import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-scroll';
import './Hero.css';
import profileImg from '../assets/profile.jpg';
import CVModal from './CVModal';

const Hero = () => {
    const [isCVOpen, setIsCVOpen] = useState(false);

    return (
        <section id="home" className="hero">
            <CVModal isOpen={isCVOpen} onClose={() => setIsCVOpen(false)} />
            <div className="container hero-container">
                <motion.div
                    className="hero-content"
                    initial={{ opacity: 0, x: -100 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.8 }}
                >
                    <h3 className="hero-subtitle">System Online...</h3>
                    <h1 className="hero-title">
                        Hello, I'm <span className="highlight">Aakash Neupane</span>
                    </h1>
                    <h2 className="hero-role">Frontend Developer & Graphic Designer</h2>
                    <p className="hero-desc">
                        Creative and adaptable individual with a background in IT and a Diploma in Computer Engineering.
                        Passionate about technology, cybersecurity, and innovative digital media projects.
                    </p>
                    <div className="hero-btns">
                        <button className="btn-primary" onClick={() => setIsCVOpen(true)}>View CV</button>
                        <Link to="contact" smooth={true} duration={500} offset={-70}>
                            <button className="btn-secondary">Establish Uplink</button>
                        </Link>
                    </div>
                </motion.div>

                <motion.div
                    className="hero-img-container"
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.8 }}
                >
                    <div className="hero-circle"></div>
                    <div className="hero-profile-box">
                        <img src={profileImg} alt="Aakash Neupane" className="profile-img" />
                    </div>
                </motion.div>
            </div>
        </section>
    );
};

export default Hero;
