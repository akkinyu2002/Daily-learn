import React from 'react';
import { FaReact, FaHtml5, FaCss3Alt, FaJs, FaPalette, FaCode, FaAndroid, FaVideo, FaFilm } from 'react-icons/fa';
// import { SiAdobephotoshop, SiAdobeillustrator, SiAdobeindesign, SiCsharp, SiVisualstudiocode } from 'react-icons/si';
import './Skills.css';

const Skills = () => {
    const skills = [
        { name: 'Graphic Design', icon: <FaPalette />, color: '#ff00ff' },
        { name: 'Frontend Dev', icon: <FaCode />, color: '#61DAFB' },
        { name: 'Photoshop', icon: <FaPalette />, color: '#31A8FF' }, // Replaced
        { name: 'Illustrator', icon: <FaPalette />, color: '#FF9A00' }, // Replaced
        { name: 'InDesign', icon: <FaPalette />, color: '#FF3366' }, // Replaced
        { name: 'React', icon: <FaReact />, color: '#61DAFB' },
        { name: 'JavaScript', icon: <FaJs />, color: '#F7DF1E' },
        { name: 'HTML5', icon: <FaHtml5 />, color: '#E34F26' },
        { name: 'CSS3', icon: <FaCss3Alt />, color: '#1572B6' },
        { name: 'C#', icon: <FaCode />, color: '#239120' }, // Replaced
        { name: 'Android Studio', icon: <FaAndroid />, color: '#3DDC84' },
        { name: 'VS Code', icon: <FaCode />, color: '#007ACC' }, // Replaced
        { name: 'Video Editing', icon: <FaVideo />, color: '#FF0000' },
        { name: '2D Animation', icon: <FaFilm />, color: '#FF9900' },
    ];

    return (
        <section id="skills" className="skills">
            <div className="container">
                <h2 className="section-title"><span>02.</span> System Modules</h2>

                <div className="skills-grid">
                    {skills.map((skill, index) => (
                        <div key={index} className="skill-card glass">
                            <div className="skill-icon" style={{ color: skill.color }}>
                                {skill.icon}
                            </div>
                            <p className="skill-name">{skill.name}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Skills;
