# Development Guide

## Project Structure

```
auto-github-builder/
├── packages/
│   ├── backend/          # Express.js server
│   ├── cli/              # Command-line tool
│   ├── web/              # React dashboard
│   └── shared/           # Shared types & utilities
├── .env.example          # Environment variables template
└── README.md             # Main documentation
```

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm 9+
- GitHub account with Personal Access Token

### Installation

1. Clone the repository
```bash
git clone <repo-url>
cd auto-github-builder
```

2. Install dependencies
```bash
npm install
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your GitHub credentials
```

### Running the Project

#### Option 1: Development Mode (All packages)
```bash
npm run dev
```

This will start:
- **Backend**: http://localhost:3001
- **Web Dashboard**: http://localhost:3000
- **CLI**: Available via `npm run dev` in `packages/cli`

#### Option 2: Individual Package Development

**Backend**
```bash
cd packages/backend
npm run dev
```

**Web Dashboard**
```bash
cd packages/web
npm run dev
```

**CLI**
```bash
cd packages/cli
npm run dev -- setup
```

### Building for Production

```bash
npm run build
```

This builds all packages into `dist/` directories.

## Key Features Implementation

### 1. Project Generation
Located in: `packages/backend/src/services/project-generator.ts`

The `ProjectGenerator` class randomly selects from templates:
- Algorithm challenges (Prime checker, Palindrome check, Fibonacci)
- Web components
- CLI tools
- Scripts
- Games
- Visualizations

### 2. GitHub Integration
Located in: `packages/backend/src/services/github.ts`

The `GitHubService` handles:
- User authentication via personal tokens
- Creating/updating files in repositories
- Fetching repository information
- Managing commits

### 3. Scheduling
Located in: `packages/backend/src/services/scheduler.ts`

Uses `node-cron` to schedule daily project generation at configured times.

### 4. CLI Commands
Located in: `packages/cli/src/commands/`

- `setup`: Configure GitHub authentication
- `generate`: Create and commit a project
- `status`: View streak statistics
- `enable`: Enable automatic daily generation

### 5. Web Dashboard
Located in: `packages/web/src/`

React app with:
- Login page (OAuth + Token)
- Dashboard with streak tracking
- Portfolio page
- Settings management

## API Endpoints

### Authentication
- `POST /api/auth/validate-token` - Validate GitHub token
- `POST /api/auth/github` - GitHub OAuth callback

### Projects
- `POST /api/projects/generate` - Generate random project
- `POST /api/projects/commit` - Commit project to GitHub
- `POST /api/projects/generate-and-commit` - One-step generation and commit

### Users
- `GET /api/users/profile/:token` - Get user profile
- `GET /api/users/:userId/streak` - Get streak statistics

### Health
- `GET /api/health` - Server health check

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  github_id INTEGER UNIQUE,
  username VARCHAR(255) UNIQUE,
  email VARCHAR(255),
  token VARCHAR(255),
  avatar_url VARCHAR(255),
  created_at TIMESTAMP
);
```

### Projects Table
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(255),
  type VARCHAR(50),
  commit_hash VARCHAR(255),
  created_at TIMESTAMP
);
```

### Streaks Table
```sql
CREATE TABLE streaks (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  current_streak INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  last_commit_date TIMESTAMP,
  updated_at TIMESTAMP
);
```

## Environment Variables

See `.env.example` for all required variables:
- `GITHUB_CLIENT_ID` - GitHub OAuth app ID
- `GITHUB_CLIENT_SECRET` - GitHub OAuth secret
- `GITHUB_API_TOKEN` - GitHub PAT for testing
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - JWT signing secret
- `PORT` - Server port (default: 3001)
- `STRIPE_SECRET_KEY` - Stripe API key (for payments)

## Testing

```bash
# Run all tests
npm run test

# Run specific package tests
cd packages/backend && npm test
```

## Deployment

### Heroku
```bash
heroku create auto-github-builder
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Docker
```bash
docker build -t auto-github-builder .
docker run -p 3001:3001 auto-github-builder
```

### AWS/Azure/GCP
See deployment guides in docs/

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit PR with description

## Troubleshooting

**"Invalid GitHub token"**
- Ensure token has `repo` and `user` scopes
- Token may have expired

**"Cannot commit to repository"**
- Ensure you have push access
- Repository may not exist (create it first)
- Check branch name is correct

**"Build errors"**
```bash
# Clean install
rm -rf node_modules
npm install
npm run build
```

## Performance Tips

1. Cache GitHub API responses
2. Batch project generation for multiple users
3. Use database indexes on frequently queried columns
4. Implement rate limiting for API endpoints

## Security Considerations

- Never commit `.env` files
- Rotate tokens regularly
- Validate all user inputs
- Use HTTPS in production
- Implement CORS properly
- Rate limit API endpoints
- Sanitize commit messages

## Resources

- [GitHub API Docs](https://docs.github.com/en/rest)
- [Node.js Best Practices](https://nodejs.org/en/docs/guides/)
- [React Documentation](https://react.dev)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Support

For issues and questions:
1. Check existing GitHub issues
2. Review documentation
3. Open new issue with reproduction steps

## License

MIT License - See LICENSE file
