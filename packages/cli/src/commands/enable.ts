import { Command } from 'commander';
import chalk from 'chalk';
import inquirer from 'inquirer';
import Conf from 'conf';

const config = new Conf({
  projectName: 'auto-github-builder',
});

const enableCommand = new Command()
  .name('enable')
  .description('Enable automatic daily project generation')
  .action(async () => {
    console.log(chalk.cyan.bold('\n⏰ Enable Daily Auto-Generation\n'));

    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'frequency',
        message: 'When should projects be generated?',
        choices: [
          { name: 'Every day at 9 AM', value: '9am' },
          { name: 'Every day at 12 PM', value: '12pm' },
          { name: 'Every day at 6 PM', value: '6pm' },
          { name: 'Custom time', value: 'custom' },
        ],
      },
    ]);

    if (answers.frequency === 'custom') {
      const customTime = await inquirer.prompt([
        {
          type: 'input',
          name: 'time',
          message: 'Enter time (HH:MM in 24-hour format):',
          validate: (input: string) => /^\d{2}:\d{2}$/.test(input) || 'Please enter time in HH:MM format',
        },
      ]);
      config.set('schedule.frequency', customTime.time);
    } else {
      config.set('schedule.frequency', answers.frequency);
    }

    config.set('schedule.enabled', true);

    console.log(chalk.green('\n✓ Daily auto-generation enabled!'));
    console.log(
      chalk.gray(
        '\nYou will receive projects at your selected time every day.'
      )
    );
    console.log(chalk.gray('Check your portfolio at: https://github.com/profile/portfolio\n'));
  });

export default enableCommand;
