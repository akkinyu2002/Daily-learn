import React from 'react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="container footer-container">
                <p>Designed & Built by <span className="highlight">Aakash</span></p>
                <p className="copyright">&copy; {new Date().getFullYear()} All Systems Operational.</p>
            </div>
        </footer>
    );
};

export default Footer;
