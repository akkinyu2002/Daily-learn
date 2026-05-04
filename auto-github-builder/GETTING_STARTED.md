# Auto GitHub Builder - Getting Started

Welcome! This guide will help you set up Auto GitHub Builder for development or use.

## Quick Start

### For Users

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/auto-github-builder.git
   cd auto-github-builder
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your GitHub token
   ```

4. **Start development servers**
   ```bash
   npm run dev
   ```

5. **Choose your interface**
   - **Web Dashboard**: http://localhost:3000
   - **CLI Tool**: Run `npm run dev --workspace=packages/cli`

### For Developers

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed setup instructions.

## First Steps

### Via CLI
```bash
# Setup GitHub authentication
npx agb setup

# Generate your first project
npx agb generate

# Check your streak
npx agb status

# Enable daily auto-generation
npx agb enable
```

### Via Web Dashboard
1. Navigate to http://localhost:3000
2. Login with GitHub Personal Access Token
3. Configure repository settings
4. Click "Generate Now" to create your first project

## Configuration

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `user`
4. Copy and paste into CLI or web dashboard

### Repository Setup
- Create a new repository for your projects (e.g., `auto-projects`)
- Auto GitHub Builder will auto-commit projects to this repo

### Schedule Configuration
Choose when projects are generated:
- Daily at 9 AM (default)
- Daily at 12 PM
- Daily at 6 PM
- Custom time

## Common Tasks

### View Your Streaks
```bash
agb status
```

### Generate Project Now
```bash
agb generate
```

### View Your Portfolio
Visit http://localhost:3000/portfolio

### Change Settings
Visit http://localhost:3000/settings

## Troubleshooting

### Issue: "Invalid GitHub token"
**Solution**: Ensure your token has `repo` and `user` scopes

### Issue: "Failed to commit to repository"
**Solution**: 
- Verify the repository exists
- Ensure you have push access
- Check the branch name (usually `main`)

### Issue: Build errors
**Solution**:
```bash
rm -rf node_modules
npm install
npm run build
```

### Issue: Port already in use
**Solution**:
```bash
# Change port in environment
PORT=3002 npm run dev
```

## Project Structure

```
📁 auto-github-builder/
├── 📁 packages/
│   ├── 📁 backend/     - Express.js server
│   ├── 📁 cli/         - Command-line tool
│   ├── 📁 web/         - React dashboard
│   └── 📁 shared/      - Shared types
├── 📄 README.md        - Main documentation
├── 📄 DEVELOPMENT.md   - Dev guide
├── 📄 PRD.md           - Product requirements
└── 📄 docker-compose.yml
```

## Key Features

### 🤖 Automated Projects
- Random project generation
- Multiple project types (algorithms, components, games, etc.)
- Configurable templates

### 📅 Smart Scheduling
- Cron-based scheduling
- Multiple time options
- Configurable frequency

### 🔥 Streak Tracking
- Current streak counter
- Longest streak record
- Total commits tracker
- Last commit date

### 📊 Portfolio Page
- Showcase generated projects
- Statistics and analytics
- Shareable links

### 💻 Flexible Access
- Web dashboard for browsing
- CLI tool for automation
- API for integrations

## Next Steps

1. **Setup**: Follow Quick Start above
2. **Explore**: Check out generated projects
3. **Customize**: Adjust settings to your preference
4. **Track**: Monitor your streaks and progress
5. **Share**: Showcase your portfolio

## Getting Help

- 📖 Read [DEVELOPMENT.md](./DEVELOPMENT.md) for technical details
- 🐛 Report issues on GitHub
- 💬 Ask questions in discussions
- 📧 Email support (when available)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - Feel free to use for personal or commercial projects.

## Roadmap

- ✅ MVP (current)
- 🔄 v1.1: Advanced analytics
- 📅 v2.0: Social features
- 🤖 v3.0: AI-powered projects

---

**Ready to start?** Run `npm install && npm run dev` and visit http://localhost:3000! 🚀
