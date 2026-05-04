declare module 'node-cron' {
  export interface ScheduleOptions {
    scheduled?: boolean;
    timezone?: string;
    name?: string;
    recoverMissedExecutions?: boolean;
    runOnInit?: boolean;
  }

  export interface ScheduledTask {
    start(): void;
    stop(): void;
    destroy(): void;
  }

  export function schedule(
    expression: string,
    task: () => void | Promise<void>,
    options?: ScheduleOptions
  ): ScheduledTask;

  export function validate(expression: string): boolean;

  const cron: {
    schedule: typeof schedule;
    validate: typeof validate;
  };

  export default cron;
}

declare module 'passport' {
  import type { RequestHandler } from 'express';

  export interface InitializeOptions {
    userProperty?: string;
    compat?: boolean;
  }

  export interface Authenticator {
    initialize(options?: InitializeOptions): RequestHandler;
  }

  const passport: Authenticator;
  export default passport;
}
