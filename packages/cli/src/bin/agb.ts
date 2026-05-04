#!/usr/bin/env node

import { Command } from 'commander';
import chalk from 'chalk';
import setupCommand from '../commands/setup.js';
import generateCommand from '../commands/generate.js';
import statusCommand from '../commands/status.js';
import enableCommand from '../commands/enable.js';

const program = new Command();

program
  .name('agb')
  .description('Auto GitHub Builder - Maintain your GitHub streaks automatically')
  .version('0.1.0');

// Setup command
program.addCommand(setupCommand);

// Generate command
program.addCommand(generateCommand);

// Status command
program.addCommand(statusCommand);

// Enable command
program.addCommand(enableCommand);

program
  .command('help')
  .description('Show help information')
  .action(() => {
    console.log(chalk.cyan.bold('\n🚀 Auto GitHub Builder\n'));
    console.log(chalk.gray('Usage: agb <command> [options]\n'));
    console.log(chalk.yellow('Commands:'));
    console.log('  setup              Configure GitHub authentication');
    console.log('  generate           Generate a new project');
    console.log('  status             Show your streak status');
    console.log('  enable             Enable daily project generation\n');
  });

program.parse(process.argv);

if (process.argv.length < 3) {
  console.log(chalk.cyan.bold('\n🚀 Auto GitHub Builder\n'));
  console.log(chalk.gray('Run "agb help" for available commands'));
  console.log(chalk.gray('Or "agb --help" for CLI options\n'));
}

export default program;
