import fs from 'fs';
import path from 'path';

const root = path.resolve('.');
const dist = path.join(root, 'dist');

if (!fs.existsSync(dist)) {
  console.error('dist/ not found. Run vite build first.');
  process.exit(1);
}

// Clean existing built assets in root
const assetsDir = path.join(root, 'assets');
if (fs.existsSync(assetsDir)) {
  fs.rmSync(assetsDir, { recursive: true, force: true });
}

// Copy dist contents to root
for (const entry of fs.readdirSync(dist)) {
  const src = path.join(dist, entry);
  const dest = path.join(root, entry);
  fs.rmSync(dest, { recursive: true, force: true });
  fs.cpSync(src, dest, { recursive: true });
}

console.log('Copied dist/* to docs root for GitHub Pages.');
