import cron from 'node-cron';
import { projectGenerator } from './project-generator.js';

interface ScheduledUser {
  id: string;
  token: string;
  owner: string;
  repo: string;
  branch: string;
}

class Scheduler {
  private jobs = new Map<string, any>();
  private scheduledUsers: ScheduledUser[] = [];

  setupScheduler() {
    console.log('📅 Setting up project generation scheduler...');

    // Run daily at 9 AM (adjust timezone as needed)
    cron.schedule('0 9 * * *', async () => {
      console.log('🤖 Generating daily projects for scheduled users...');
      await this.generateDailyProjects();
    });

    console.log('✓ Scheduler initialized');
  }

  private async generateDailyProjects() {
    for (const user of this.scheduledUsers) {
      try {
        const project = projectGenerator.generateDailyProject();
        await projectGenerator.commitProject(
          user.token,
          user.owner,
          user.repo,
          user.branch,
          project
        );
        console.log(`✓ Project generated for ${user.owner}/${user.repo}`);
      } catch (error) {
        console.error(`✗ Failed to generate project for ${user.owner}/${user.repo}:`, error);
      }
    }
  }

  addUser(user: ScheduledUser) {
    this.scheduledUsers.push(user);
  }

  removeUser(userId: string) {
    this.scheduledUsers = this.scheduledUsers.filter((u) => u.id !== userId);
  }
}

const scheduler = new Scheduler();

export function setupScheduler() {
  scheduler.setupScheduler();
}

export { scheduler };
