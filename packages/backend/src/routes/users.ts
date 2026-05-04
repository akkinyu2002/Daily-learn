import express from 'express';
import { GitHubService } from '../services/github.js';

const router = express.Router();

// Get user profile
router.get('/profile/:token', async (req, res) => {
  try {
    const { token } = req.params;

    const user = await GitHubService.getUserInfo(token);
    const repos = await GitHubService.getUserRepositories(token, 5);

    res.json({
      success: true,
      user: {
        id: user.id,
        login: user.login,
        avatar_url: user.avatar_url,
        bio: user.bio,
        public_repos: user.public_repos,
      },
      recentRepos: repos.map((r: any) => ({
        id: r.id,
        name: r.name,
        url: r.html_url,
        description: r.description,
      })),
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch user profile' });
  }
});

// Get streak stats (mock for now)
router.get('/:userId/streak', (req, res) => {
  res.json({
    success: true,
    streak: {
      current: Math.floor(Math.random() * 100),
      longest: Math.floor(Math.random() * 365),
      totalCommits: Math.floor(Math.random() * 1000),
    },
  });
});

export default router;
