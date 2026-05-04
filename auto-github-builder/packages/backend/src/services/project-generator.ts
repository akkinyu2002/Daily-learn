import { GitHubService } from './github.js';

interface ProjectTemplate {
  name: string;
  description: string;
  type: 'algorithm' | 'component' | 'script' | 'game' | 'visualization' | 'cli';
  generateContent: () => string;
  filename: string;
}

class ProjectGenerator {
  private templates: ProjectTemplate[] = [
    {
      name: 'Prime Checker',
      description: 'Check if a number is prime',
      type: 'algorithm',
      filename: 'prime-checker.js',
      generateContent: () => `
function isPrime(num) {
  if (num <= 1) return false;
  if (num <= 3) return true;
  if (num % 2 === 0 || num % 3 === 0) return false;
  
  for (let i = 5; i * i <= num; i += 6) {
    if (num % i === 0 || num % (i + 2) === 0) return false;
  }
  return true;
}

console.log(isPrime(17)); // true
console.log(isPrime(20)); // false
`,
    },
    {
      name: 'Palindrome Check',
      description: 'Check if a string is a palindrome',
      type: 'algorithm',
      filename: 'palindrome.js',
      generateContent: () => `
function isPalindrome(str) {
  const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
  return cleaned === cleaned.split('').reverse().join('');
}

console.log(isPalindrome('A man, a plan, a canal: Panama')); // true
console.log(isPalindrome('hello')); // false
`,
    },
    {
      name: 'Fibonacci Generator',
      description: 'Generate Fibonacci sequence',
      type: 'algorithm',
      filename: 'fibonacci.js',
      generateContent: () => `
function fibonacci(n) {
  if (n <= 0) return [];
  if (n === 1) return [0];
  
  const seq = [0, 1];
  for (let i = 2; i < n; i++) {
    seq.push(seq[i - 1] + seq[i - 2]);
  }
  return seq;
}

console.log(fibonacci(10));
// Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
`,
    },
    {
      name: 'Todo List CLI',
      description: 'Simple command-line todo manager',
      type: 'cli',
      filename: 'todo-cli.js',
      generateContent: () => `
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const todoFile = path.join(process.env.HOME, '.todos.json');

function loadTodos() {
  try {
    return JSON.parse(fs.readFileSync(todoFile, 'utf-8'));
  } catch {
    return [];
  }
}

function saveTodos(todos) {
  fs.writeFileSync(todoFile, JSON.stringify(todos, null, 2));
}

const command = process.argv[2];
const todos = loadTodos();

if (command === 'add') {
  todos.push({ id: Date.now(), text: process.argv.slice(3).join(' '), done: false });
  console.log('✓ Todo added');
} else if (command === 'list') {
  todos.forEach((todo, i) => {
    console.log(\`\${todo.done ? '✓' : '○'} [\${i}] \${todo.text}\`);
  });
}

saveTodos(todos);
`,
    },
    {
      name: 'Color Contrast Checker',
      description: 'Utility to check color contrast ratios',
      type: 'script',
      filename: 'color-contrast.js',
      generateContent: () => `
function hexToRgb(hex) {
  const result = /^#?([a-f\\d]{2})([a-f\\d]{2})([a-f\\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function getLuminance(rgb) {
  const [r, g, b] = [rgb.r, rgb.g, rgb.b].map(x => {
    x = x / 255;
    return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function getContrast(hex1, hex2) {
  const rgb1 = hexToRgb(hex1);
  const rgb2 = hexToRgb(hex2);
  const lum1 = getLuminance(rgb1);
  const lum2 = getLuminance(rgb2);
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

console.log(getContrast('#000000', '#FFFFFF')); // 21:1
console.log(getContrast('#777777', '#FFFFFF')); // ~4.5:1
`,
    },
  ];

  getRandomProject(): ProjectTemplate {
    return this.templates[Math.floor(Math.random() * this.templates.length)];
  }

  generateDailyProject() {
    const template = this.getRandomProject();
    return {
      ...template,
      timestamp: new Date(),
      content: template.generateContent(),
    };
  }

  async commitProject(
    token: string,
    owner: string,
    repo: string,
    branch: string,
    project: any
  ): Promise<void> {
    const date = new Date().toISOString().split('T')[0];
    const fileName = `projects/${date}-${project.filename}`;
    const commitMessage = `chore: add ${project.name} project for ${date}`;

    await GitHubService.createOrUpdateFile({
      owner,
      repo,
      branch,
      path: fileName,
      content: project.content,
      message: commitMessage,
      token,
    });
  }
}

export const projectGenerator = new ProjectGenerator();
export default ProjectGenerator;
