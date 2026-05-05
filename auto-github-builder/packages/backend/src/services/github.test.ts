import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { Mock } from 'vitest';
import axios from 'axios';
import { GitHubService } from './github.js';

vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    put: vi.fn(),
    isAxiosError: vi.fn(() => false),
  },
}));

const mockedAxios = axios as unknown as {
  get: Mock;
  put: Mock;
  isAxiosError: Mock;
};

describe('GitHubService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('loads content metadata so existing files can be updated with their sha', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { sha: 'existing-file-sha' } });
    mockedAxios.put.mockResolvedValueOnce({ data: {} });

    await GitHubService.createOrUpdateFile({
      owner: 'octocat',
      repo: 'auto-projects',
      branch: 'main',
      path: 'projects/example.js',
      content: 'console.log("hello");',
      message: 'chore: add example',
      token: 'github-token',
    });

    expect(mockedAxios.get).toHaveBeenCalledWith(
      'https://api.github.com/repos/octocat/auto-projects/contents/projects/example.js?ref=main',
      {
        headers: {
          Authorization: 'token github-token',
          Accept: 'application/vnd.github.v3+json',
        },
      }
    );

    expect(mockedAxios.put).toHaveBeenCalledWith(
      'https://api.github.com/repos/octocat/auto-projects/contents/projects/example.js',
      expect.objectContaining({
        sha: 'existing-file-sha',
        content: Buffer.from('console.log("hello");').toString('base64'),
      }),
      expect.any(Object)
    );
  });
});
