// User Types
export interface User {
  id: string;
  username: string;
  avatar_url: string;
  bio?: string;
  public_repos: number;
}

export interface AuthToken {
  token: string;
  user: User;
}

// Project Types
export type ProjectType = 'algorithm' | 'component' | 'script' | 'game' | 'visualization' | 'cli';

export interface Project {
  id: string;
  name: string;
  description: string;
  type: ProjectType;
  content: string;
  filename: string;
  timestamp: Date;
  commitHash?: string;
}

export interface ProjectTemplate {
  name: string;
  description: string;
  type: ProjectType;
  filename: string;
  generateContent: () => string;
}

// Streak Types
export interface Streak {
  current: number;
  longest: number;
  totalCommits: number;
  lastCommitDate?: Date;
}

// GitHub Types
export interface GitHubRepository {
  id: number;
  name: string;
  url: string;
  description?: string;
  stars: number;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Configuration Types
export interface AppConfig {
  github: {
    token: string;
    username: string;
    repo: string;
    branch: string;
  };
  schedule: {
    enabled: boolean;
    frequency: string; // '9am', '12pm', '6pm', or custom 'HH:MM'
  };
}
