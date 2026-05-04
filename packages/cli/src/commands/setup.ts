import { Command } from 'commander';
import chalk from 'chalk';
import inquirer from 'inquirer';
import ora from 'ora';
import Conf from 'conf';
import axios from 'axios';

const config = new Conf({
  projectName: 'auto-github-builder',
});

const setupCommand = new Command()
  .name('setup')
  .description('Configure GitHub authentication')
  .action(async () => {
    console.log(chalk.cyan.bold('\n⚙️  Setup GitHub Authentication\n'));

    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'authMethod',
        message: 'How would you like to authenticate?',
        choices: [
          { name: 'Personal Access Token (Recommended)', value: 'token' },
          { name: 'GitHub OAuth', value: 'oauth' },
        ],
      },
    ]);

    if (answers.authMethod === 'token') {
      const tokenAnswers = await inquirer.prompt([
        {
          type: 'password',
          name: 'token',
          message: 'Enter your GitHub Personal Access Token:',
          mask: '*',
        },
      ]);

      const spinner = ora('Validating token...').start();

      try {
        // Validate token with backend
        const response = await axios.post(
          'http://localhost:3001/api/auth/validate-token',
          { token: tokenAnswers.token }
        );

        config.set('github.token', tokenAnswers.token);
        config.set('github.username', response.data.user.login);

        spinner.succeed(
          chalk.green(`✓ Authenticated as @${response.data.user.login}`)
        );
        console.log(
          chalk.gray(
            `\nPublic repos: ${response.data.user.public_repos}`
          )
        );
      } catch (error) {
        spinner.fail('Invalid token');
      }
    }

    // Configure repository
    const repoAnswers = await inquirer.prompt([
      {
        type: 'input',
        name: 'repo',
        message: 'GitHub repository name (leave blank to create new):',
      },
      {
        type: 'input',
        name: 'branch',
        message: 'Branch name:',
        default: 'main',
      },
    ]);

    config.set('github.repo', repoAnswers.repo || 'auto-projects');
    config.set('github.branch', repoAnswers.branch);

    console.log(chalk.green('\n✓ Setup complete!\n'));
    console.log(chalk.gray('Next steps:'));
    console.log('  agb generate    - Generate a project');
    console.log('  agb status      - View your streak\n');
  });

export default setupCommand;
