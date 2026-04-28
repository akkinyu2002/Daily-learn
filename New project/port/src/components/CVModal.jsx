import React from 'react';
import { FaTimes, FaDownload } from 'react-icons/fa';
import './CVModal.css';
import cv1 from '../assets/cv-1.jpg';
import cv2 from '../assets/cv-2.jpg';

const CVModal = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="cv-modal-overlay" onClick={onClose}>
            <div className="cv-modal-content" onClick={e => e.stopPropagation()}>
                <button className="cv-close-btn" onClick={onClose}>
                    <FaTimes />
                </button>

                <h2 className="cv-title">Mission Documentation</h2>

                <div className="cv-pages">
                    <div className="cv-page">
                        <img src={cv1} alt="CV Page 1" />
                        <a href={cv1} download="Aakash_Neupane_CV_Page1.jpg" className="cv-download-btn">
                            <FaDownload /> Download Page 1
                        </a>
                    </div>
                    <div className="cv-page">
                        <img src={cv2} alt="CV Page 2" />
                        <a href={cv2} download="Aakash_Neupane_CV_Page2.jpg" className="cv-download-btn">
                            <FaDownload /> Download Page 2
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CVModal;
