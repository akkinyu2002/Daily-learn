# Auto GitHub Builder 🚀

A tool for students and developers to maintain GitHub streaks with automated daily projects and commits.

## Features

- 🤖 **Automated Project Generation**: Creates diverse small projects daily
- 📅 **Scheduled Commits**: Auto-commits with meaningful messages
- 🔥 **Streak Tracking**: Monitor your GitHub activity streaks
- 📊 **Portfolio Dashboard**: Beautiful portfolio page showcasing your work
- 🔐 **Flexible Auth**: GitHub OAuth or Personal Access Tokens
- 💻 **CLI + Web**: Command-line tool and web dashboard

## Architecture

This is a monorepo with the following packages:

### `packages/backend`
Express.js server handling:
- GitHub API integration
- Project generation logic
- Scheduling and automation
- User authentication
- Database management

### `packages/cli`
Command-line interface for:
- Local configuration setup
- Manual project generation
- Viewing streak status
- Direct GitHub authentication

### `packages/web`
React dashboard for:
- User authentication
- Streak tracking visualization
- Portfolio page
- Settings management

### `packages/shared`
Shared TypeScript types and utilities

## Getting Started

### Prerequisites
- Node.js 18+
- npm 9+
- GitHub account

### Installation

```bash
# Install dependencies
npm install

# Setup environment variables
cp .env.example .env

# Start development servers
npm run dev
```

## Project Types Generated

The tool generates a mix of:
- **Algorithm Challenges**: Coding problems with solutions
- **Web Components**: React/Vue components
- **Scripts**: Utility scripts and tools
- **Games**: Simple interactive projects
- **Data Visualizations**: Charts and visualizations
- **CLI Tools**: Command-line utilities

## Monetization

- **Free Tier**: 1 project per month, basic portfolio
- **Pro Tier** ($4.99/month): Daily projects, advanced portfolio, custom templates
- **Enterprise**: Custom project generation, team management

## Development

```bash
# Run in development mode with hot reload
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Format code
npm run format
```

## License

MIT
