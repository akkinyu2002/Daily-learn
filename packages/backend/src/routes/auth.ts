import express from 'express';
import axios from 'axios';
import { GitHubService } from '../services/github.js';

const router = express.Router();

const GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize';
const GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token';
const DEFAULT_FRONTEND_URL = 'http://localhost:3000';
const DEFAULT_CALLBACK_URL = 'http://localhost:3001/api/auth/github/callback';

function getFrontendUrl() {
  return process.env.FRONTEND_URL || DEFAULT_FRONTEND_URL;
}

function getCallbackUrl() {
  return process.env.GITHUB_CALLBACK_URL || DEFAULT_CALLBACK_URL;
}

function redirectToFrontend(res: express.Response, params: Record<string, string>) {
  const url = new URL('/auth/github/callback', getFrontendUrl());

  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, value);
  });

  res.redirect(url.toString());
}

// Start GitHub OAuth in the browser.
router.get('/github', (_req, res) => {
  const clientId = process.env.GITHUB_CLIENT_ID;

  if (!clientId) {
    redirectToFrontend(res, {
      error: 'GitHub OAuth is not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET.',
    });
    return;
  }

  const url = new URL(GITHUB_AUTHORIZE_URL);
  url.searchParams.set('client_id', clientId);
  url.searchParams.set('redirect_uri', getCallbackUrl());
  url.searchParams.set('scope', 'repo read:user user:email');

  res.redirect(url.toString());
});

// Handle the GitHub OAuth redirect and exchange the code for an access token.
router.get('/github/callback', async (req, res) => {
  try {
    const code = typeof req.query.code === 'string' ? req.query.code : undefined;

    if (!code) {
      redirectToFrontend(res, { error: 'Missing authorization code from GitHub.' });
      return;
    }

    const clientId = process.env.GITHUB_CLIENT_ID;
    const clientSecret = process.env.GITHUB_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
      redirectToFrontend(res, {
        error: 'GitHub OAuth is not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET.',
      });
      return;
    }

    const tokenResponse = await axios.post(
      GITHUB_TOKEN_URL,
      {
        client_id: clientId,
        client_secret: clientSecret,
        code,
        redirect_uri: getCallbackUrl(),
      },
      {
        headers: {
          Accept: 'application/json',
        },
      }
    );

    const accessToken = tokenResponse.data.access_token;

    if (!accessToken) {
      redirectToFrontend(res, { error: 'GitHub did not return an access token.' });
      return;
    }

    const user = await GitHubService.getUserInfo(accessToken);

    redirectToFrontend(res, {
      token: accessToken,
      username: user.login,
    });
  } catch (error) {
    console.error('GitHub OAuth error:', error);
    redirectToFrontend(res, { error: 'GitHub authentication failed.' });
  }
});

// Exchange a GitHub OAuth code from an API client.
router.post('/github', async (req, res) => {
  try {
    const { code } = req.body;

    if (!code) {
      return res.status(400).json({ error: 'Missing authorization code' });
    }

    const clientId = process.env.GITHUB_CLIENT_ID;
    const clientSecret = process.env.GITHUB_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
      return res.status(500).json({
        error: 'GitHub OAuth is not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET.',
      });
    }

    const tokenResponse = await axios.post(
      GITHUB_TOKEN_URL,
      {
        client_id: clientId,
        client_secret: clientSecret,
        code,
        redirect_uri: getCallbackUrl(),
      },
      {
        headers: {
          Accept: 'application/json',
        },
      }
    );

    const accessToken = tokenResponse.data.access_token;

    if (!accessToken) {
      return res.status(502).json({ error: 'GitHub did not return an access token' });
    }

    const user = await GitHubService.getUserInfo(accessToken);

    res.json({
      success: true,
      token: accessToken,
      user: {
        id: user.id,
        login: user.login,
        avatar_url: user.avatar_url,
        public_repos: user.public_repos,
      },
    });
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
});

// Validate personal access token
router.post('/validate-token', async (req, res) => {
  try {
    const { token } = req.body;

    if (!token) {
      return res.status(400).json({ error: 'Missing token' });
    }

    const user = await GitHubService.getUserInfo(token);

    res.json({
      success: true,
      user: {
        id: user.id,
        login: user.login,
        avatar_url: user.avatar_url,
        public_repos: user.public_repos,
      },
    });
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
});

export default router;
