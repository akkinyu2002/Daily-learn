import { Command } from 'commander';
import chalk from 'chalk';
import Conf from 'conf';
import axios from 'axios';

const config = new Conf({
  projectName: 'auto-github-builder',
});

const statusCommand = new Command()
  .name('status')
  .description('Display your streak and portfolio stats')
  .action(async () => {
    const token = config.get('github.token') as string;
    const username = config.get('github.username') as string;

    if (!token) {
      console.log(chalk.red('\n✗ GitHub token not configured'));
      console.log(chalk.gray('Run "agb setup" first\n'));
      return;
    }

    try {
      const response = await axios.get(
        `http://localhost:3001/api/users/${username}/streak`
      );

      console.log(chalk.cyan.bold('\n📊 Your GitHub Stats\n'));
      console.log(chalk.yellow(`Current Streak: ${chalk.bold(response.data.streak.current)} days 🔥`));
      console.log(chalk.yellow(`Longest Streak: ${chalk.bold(response.data.streak.longest)} days`));
      console.log(chalk.yellow(`Total Commits: ${chalk.bold(response.data.streak.totalCommits)}`));
      console.log();
    } catch (error) {
      console.log(chalk.red('\n✗ Failed to fetch stats\n'));
    }
  });

export default statusCommand;
