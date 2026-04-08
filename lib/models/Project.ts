import mongoose, { Schema, Document } from 'mongoose';

export interface IProject extends Document {
    title: string;
    description: string;
    category: 'Video Editing' | 'Graphic Design' | 'Motion Graphics' | 'Social Media';
    thumbnail: string;
    mediaUrls: string[];
    videoUrl?: string;
    toolsUsed: string[];
    client?: string;
    duration?: string;
    isFeatured: boolean;
    createdAt: Date;
}

const ProjectSchema: Schema = new Schema({
    title: { type: String, required: true },
    description: { type: String, required: true },
    category: {
        type: String,
        required: true,
        enum: ['Video Editing', 'Graphic Design', 'Motion Graphics', 'Social Media']
    },
    thumbnail: { type: String, required: true },
    mediaUrls: [{ type: String }],
    videoUrl: { type: String },
    toolsUsed: [{ type: String }],
    client: { type: String },
    duration: { type: String },
    isFeatured: { type: Boolean, default: false },
    createdAt: { type: Date, default: Date.now }
});

export default mongoose.models.Project || mongoose.model<IProject>('Project', ProjectSchema);
