// Utility functions

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
}

export function getStreakEmoji(days: number): string {
  if (days === 0) return '⭕';
  if (days < 7) return '🔥';
  if (days < 30) return '🔥🔥';
  if (days < 100) return '🔥🔥🔥';
  return '🔥🔥🔥🔥';
}

export function getRandomItem<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
