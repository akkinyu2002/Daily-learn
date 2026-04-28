import React from 'react';
import { FaEnvelope, FaLinkedin, FaGithub, FaPhone, FaMapMarkerAlt, FaBehance } from 'react-icons/fa';
import './Contact.css';

const Contact = () => {
    return (
        <section id="contact" className="contact">
            <div className="container">
                <h2 className="section-title"><span>04.</span> Establish Uplink</h2>

                <div className="contact-content">
                    <div className="contact-info glass">
                        <h3>Initialize Connection</h3>
                        <p>
                            I am currently open for new opportunities and collaborations.
                            Whether you have a question or just want to say hi, my inbox is always open.
                        </p>

                        <div className="contact-details">
                            <div className="contact-item">
                                <FaEnvelope className="contact-icon" />
                                <span>neupaneakash687@gmail.com</span>
                            </div>
                            <div className="contact-item">
                                <FaPhone className="contact-icon" />
                                <span>+977 9860212330</span>
                            </div>
                            <div className="contact-item">
                                <FaMapMarkerAlt className="contact-icon" />
                                <span>Satyawati-6, Johang, Gulmi</span>
                            </div>
                        </div>

                        <div className="social-links">
                            <a href="https://linkedin.com/in/aakash-neupane-4bb97031a" target="_blank" rel="noopener noreferrer" className="social-icon"><FaLinkedin /></a>
                            <a href="https://www.behance.net/akashneupane5" target="_blank" rel="noopener noreferrer" className="social-icon"><FaBehance /></a>
                            <a href="#" className="social-icon"><FaGithub /></a>
                        </div>
                    </div>

                    <form className="contact-form glass">
                        <div className="form-group">
                            <input type="text" placeholder="Name" required />
                        </div>
                        <div className="form-group">
                            <input type="email" placeholder="Email" required />
                        </div>
                        <div className="form-group">
                            <textarea placeholder="Message" rows="5" required></textarea>
                        </div>
                        <button type="submit" className="btn-primary">Send Transmission</button>
                    </form>
                </div>
            </div>
        </section>
    );
};

export default Contact;
