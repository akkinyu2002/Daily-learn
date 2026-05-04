# Contributing to Auto GitHub Builder

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

- Be respectful to all contributors
- Welcome beginners and provide constructive feedback
- Focus on code quality and user experience

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/auto-github-builder.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install dependencies: `npm install`
5. Start developing: `npm run dev`

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/add-new-feature
   ```

2. **Make your changes**
   - Follow existing code style
   - Write clear commit messages
   - Add tests for new features

3. **Test your changes**
   ```bash
   npm run test
   npm run build
   ```

4. **Lint and format**
   ```bash
   npm run lint
   npm run format
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/add-new-feature
   ```

## Commit Messages

Use clear, descriptive commit messages:
```
feat: add new feature name
fix: resolve issue description
docs: update documentation
style: format code
refactor: improve code structure
test: add tests
chore: maintenance tasks
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Create PR with clear description
5. Respond to review feedback
6. Squash commits before merging

## Adding New Features

### New Project Template

1. Edit `packages/backend/src/services/project-generator.ts`
2. Add to `templates` array:
```typescript
{
  name: 'Feature Name',
  description: 'Feature description',
  type: 'algorithm', // or other type
  filename: 'feature-name.js',
  generateContent: () => `// Your code here`,
}
```

### New CLI Command

1. Create file in `packages/cli/src/commands/`
2. Export Command from `src/bin/agb.ts`
3. Add tests in same folder

### New API Endpoint

1. Create route file in `packages/backend/src/routes/`
2. Import in `src/index.ts`
3. Document in README
4. Add tests in `__tests__/` folder

## Testing

```bash
# Run all tests
npm run test

# Run specific test
npm test packages/backend -- project-generator.test.ts

# Test with coverage
npm run test -- --coverage
```

## Code Style

- Use TypeScript for type safety
- Follow existing naming conventions
- Use 2-space indentation
- Keep functions small and focused
- Add JSDoc comments for public APIs

## Documentation

- Update README.md for major changes
- Add inline comments for complex logic
- Include examples for new features
- Update DEVELOPMENT.md if needed

## Performance Considerations

- Minimize GitHub API calls
- Use caching where appropriate
- Avoid blocking operations
- Test with large datasets

## Security Guidelines

- Never commit secrets or tokens
- Validate all user inputs
- Use HTTPS in production
- Follow OWASP best practices
- Report security issues privately

## Reporting Issues

Include:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Node version, etc.)
- Error messages or logs

## Feature Requests

Include:
- Description of the feature
- Use case and benefits
- Proposed implementation (optional)
- Examples or mockups

## Review Process

1. Code review from maintainers
2. Automated tests must pass
3. No merge conflicts
4. Documentation updated
5. Approval from at least 1 maintainer

## Release Process

1. Update version in package.json
2. Update CHANGELOG.md
3. Create git tag
4. Push to main
5. Publish to npm

## Areas for Contribution

- 🎨 UI/UX improvements
- 🐛 Bug fixes
- 📖 Documentation
- ✨ New features
- 🚀 Performance optimization
- 🧪 Testing
- 🔒 Security improvements

## Questions?

- Check existing issues and discussions
- Ask in GitHub discussions
- Email maintainers

## License

By contributing, you agree your code will be under MIT License.

Thank you for contributing! 🙌
