import fs from 'fs';
import path from 'path';

const root = path.resolve('.');
const src = path.join(root, 'index.source.html');
const dest = path.join(root, 'index.html');

if (!fs.existsSync(src)) {
  console.error('index.source.html not found.');
  process.exit(1);
}

fs.copyFileSync(src, dest);
console.log('Restored source index.html for Vite build.');
