import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import Conf from 'conf';
import axios from 'axios';

const config = new Conf({
  projectName: 'auto-github-builder',
});

const generateCommand = new Command()
  .name('generate')
  .description('Generate a new project and commit to GitHub')
  .action(async () => {
    const token = config.get('github.token') as string;
    const repo = config.get('github.repo') as string;
    const branch = config.get('github.branch') as string;
    const username = config.get('github.username') as string;

    if (!token) {
      console.log(chalk.red('\n✗ GitHub token not configured'));
      console.log(chalk.gray('Run "agb setup" first\n'));
      return;
    }

    const spinner = ora('Generating project...').start();

    try {
      const response = await axios.post(
        'http://localhost:3001/api/projects/generate-and-commit',
        {
          token,
          owner: username,
          repo,
          branch,
        }
      );

      spinner.succeed(
        chalk.green(`✓ Project generated and committed!`)
      );
      console.log(chalk.gray(`\nProject: ${response.data.project.name}`));
      console.log(chalk.gray(`Type: ${response.data.project.type}`));
      console.log(chalk.gray(`Repository: ${username}/${repo}\n`));
    } catch (error: any) {
      spinner.fail('Failed to generate project');
      console.log(
        chalk.red(
          `\nError: ${error.response?.data?.error || error.message}`
        )
      );
    }
  });

export default generateCommand;
