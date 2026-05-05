import axios from 'axios';

interface GitHubUser {
  id: number;
  login: string;
  avatar_url: string;
  bio?: string;
  public_repos: number;
}

interface CommitOptions {
  owner: string;
  repo: string;
  branch: string;
  path: string;
  content: string;
  message: string;
  token: string;
}

const GITHUB_API_BASE = 'https://api.github.com';

export class GitHubService {
  static async getUserInfo(token: string): Promise<GitHubUser> {
    const response = await axios.get(`${GITHUB_API_BASE}/user`, {
      headers: {
        Authorization: `token ${token}`,
        Accept: 'application/vnd.github.v3+json',
      },
    });
    return response.data;
  }

  static async createOrUpdateFile(options: CommitOptions): Promise<void> {
    const {
      owner,
      repo,
      branch,
      path,
      content,
      message,
      token,
    } = options;

    try {
      // Get the current file (if exists) to get its SHA
      let sha: string | undefined;
      try {
        const response = await axios.get(
          `${GITHUB_API_BASE}/repos/${owner}/${repo}/contents/${path}?ref=${branch}`,
          {
            headers: {
              Authorization: `token ${token}`,
              Accept: 'application/vnd.github.v3+json',
            },
          }
        );
        sha = response.data.sha;
      } catch (error) {
        // File doesn't exist, that's fine
      }

      // Create or update the file
      await axios.put(
        `${GITHUB_API_BASE}/repos/${owner}/${repo}/contents/${path}`,
        {
          message,
          content: Buffer.from(content).toString('base64'),
          branch,
          ...(sha && { sha }),
        },
        {
          headers: {
            Authorization: `token ${token}`,
            Accept: 'application/vnd.github.v3+json',
          },
        }
      );

      console.log(`✓ Committed: ${path} to ${repo}`);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(`Failed to commit: ${error.message}`);
        if (error.response?.data) {
          console.error(error.response.data);
        }
      }
      throw error;
    }
  }

  static async getUserRepositories(token: string, limit: number = 10): Promise<any[]> {
    const response = await axios.get(`${GITHUB_API_BASE}/user/repos`, {
      headers: {
        Authorization: `token ${token}`,
        Accept: 'application/vnd.github.v3+json',
      },
      params: {
        sort: 'updated',
        per_page: limit,
      },
    });
    return response.data;
  }

  static async getRepositoryInfo(
    token: string,
    owner: string,
    repo: string
  ): Promise<any> {
    const response = await axios.get(
      `${GITHUB_API_BASE}/repos/${owner}/${repo}`,
      {
        headers: {
          Authorization: `token ${token}`,
          Accept: 'application/vnd.github.v3+json',
        },
      }
    );
    return response.data;
  }
}

export default GitHubService;
