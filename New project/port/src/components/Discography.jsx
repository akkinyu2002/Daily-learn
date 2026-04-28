import React from 'react';
import { motion } from 'framer-motion';
import './Discography.css';
import album1 from '../assets/album_cover_1_1768206168894.png';
import album2 from '../assets/album_cover_2_1768206182774.png';
import album3 from '../assets/album_cover_3_1768206206480.png';
import album4 from '../assets/album_cover_4_1768206224522.png';

const Discography = () => {
    const albums = [
        {
            title: 'Digital Dreams',
            year: '2024',
            type: 'Album',
            tracks: 12,
            image: album1,
            description: 'A journey through modern soundscapes and digital emotions.'
        },
        {
            title: 'Sunset Memories',
            year: '2023',
            type: 'EP',
            tracks: 6,
            image: album2,
            description: 'Warm melodies capturing fleeting moments of golden hour.'
        },
        {
            title: 'Neon Nights',
            year: '2023',
            type: 'Single',
            tracks: 3,
            image: album3,
            description: 'Electric vibes for the late-night city wanderers.'
        },
        {
            title: 'Echoes',
            year: '2022',
            type: 'Album',
            tracks: 10,
            image: album4,
            description: 'Minimalist compositions exploring space and silence.'
        },
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.15
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 30 },
        visible: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.6,
                ease: [0.4, 0, 0.2, 1]
            }
        }
    };

    return (
        <section id="discography" className="discography">
            <div className="container">
                <h2 className="section-title"><span>04.</span> Discography</h2>

                <motion.div
                    className="albums-grid"
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, margin: "-100px" }}
                >
                    {albums.map((album, index) => (
                        <motion.div
                            key={index}
                            className="album-card glass"
                            variants={itemVariants}
                        >
                            <div className="album-image-wrapper">
                                <img src={album.image} alt={album.title} className="album-image" />
                                <div className="album-overlay">
                                    <div className="album-info">
                                        <p className="album-description">{album.description}</p>
                                        <div className="album-meta">
                                            <span>{album.tracks} tracks</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="album-details">
                                <div className="album-header">
                                    <h3 className="album-title">{album.title}</h3>
                                    <span className="album-type">{album.type}</span>
                                </div>
                                <p className="album-year">{album.year}</p>
                            </div>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
};

export default Discography;
