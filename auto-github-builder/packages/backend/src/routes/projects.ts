import express from 'express';
import { projectGenerator } from '../services/project-generator.js';

const router = express.Router();

// Generate a random project
router.post('/generate', async (req, res) => {
  try {
    const project = projectGenerator.generateDailyProject();
    res.json({
      success: true,
      project: {
        name: project.name,
        description: project.description,
        type: project.type,
        filename: project.filename,
        content: project.content,
      },
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate project' });
  }
});

// Commit a project to GitHub
router.post('/commit', async (req, res) => {
  try {
    const { token, owner, repo, branch = 'main', project } = req.body;

    if (!token || !owner || !repo || !project) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    await projectGenerator.commitProject(token, owner, repo, branch, project);

    res.json({
      success: true,
      message: 'Project committed successfully',
    });
  } catch (error) {
    console.error('Commit error:', error);
    res.status(500).json({ error: 'Failed to commit project' });
  }
});

// Generate and commit in one go
router.post('/generate-and-commit', async (req, res) => {
  try {
    const { token, owner, repo, branch = 'main' } = req.body;

    if (!token || !owner || !repo) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Generate project
    const project = projectGenerator.generateDailyProject();

    // Commit to GitHub
    await projectGenerator.commitProject(token, owner, repo, branch, project);

    res.json({
      success: true,
      message: 'Project generated and committed',
      project: {
        name: project.name,
        type: project.type,
      },
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to generate and commit project' });
  }
});

export default router;
