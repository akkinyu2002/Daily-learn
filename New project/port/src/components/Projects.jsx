import React from 'react';
import { FaGithub, FaExternalLinkAlt } from 'react-icons/fa';
import './Projects.css';
import projectPortfolio from '../assets/project-portfolio.png';
import projectMess from '../assets/project-mess.png';
import projectGraphic from '../assets/project-graphic.jpg';

const Projects = () => {
    const projects = [
        {
            title: 'Portfolio Website',
            desc: 'Designed and developed my own portfolio website and hosted it. A showcase of my skills and projects.',
            tech: ['React', 'CSS', 'Vite'],
            github: '#',
            live: 'https://www.neupaneakash.com.np/',
            image: projectPortfolio
        },
        {
            title: 'Hostel Mess Management',
            desc: 'A Windows application for managing hostel mess operations. Developed as part of academic coursework.',
            tech: ['C#', 'Visual Studio', 'SQL'],
            github: '#',
            live: '#',
            image: projectMess
        },
        {
            title: 'Graphic Design Portfolio',
            desc: 'Diverse graphic design projects including logos, posters, and social media visuals.',
            tech: ['Photoshop', 'Illustrator', 'InDesign'],
            github: '#',
            live: 'https://www.behance.net/akashneupane5',
            image: projectGraphic
        },
    ];

    return (
        <section id="projects" className="projects">
            <div className="container">
                <h2 className="section-title"><span>03.</span> Mission Logs</h2>

                <div className="projects-grid">
                    {projects.map((project, index) => (
                        <div key={index} className="project-card glass">
                            <div className="project-img">
                                <img src={project.image} alt={project.title} />
                                <div className="project-links">
                                    <a href={project.github} target="_blank" rel="noopener noreferrer"><FaGithub /></a>
                                    <a href={project.live} target="_blank" rel="noopener noreferrer"><FaExternalLinkAlt /></a>
                                </div>
                            </div>
                            <div className="project-content">
                                <h3 className="project-title">{project.title}</h3>
                                <p className="project-desc">{project.desc}</p>
                                <div className="project-tech">
                                    {project.tech.map((t, i) => (
                                        <span key={i} className="tech-tag">{t}</span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Projects;
