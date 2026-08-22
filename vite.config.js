import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadEnv } from 'vite';

const projectRoot = fileURLToPath(new URL('.', import.meta.url));

const pageNames = [
  'index',
  'register',
  'dashboard',
  'chat',
  'courses',
  'learning-plan',
  'learning-progress',
  'learning-roadmap',
  'skill-intelligence',
  'skill-recommendations',
  'skill-roadmap',
  'student-profile',
];

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiUrl = env.VITE_API_URL || '';

  return {
    plugins: [
      react(),
      {
        name: 'inject-api-config',
        transformIndexHtml(html) {
          return {
            html: apiUrl ? html.replaceAll('http://ai-student-support-career-platform-4.onrender.com', apiUrl) : html,
            tags: [{
              tag: 'script',
              children: `window.__API_BASE__ = ${JSON.stringify(apiUrl)};`,
              injectTo: 'head',
            }],
          };
        },
        generateBundle() {
          for (const assetName of ['script.js', 'styles.css']) {
            this.emitFile({
              type: 'asset',
              fileName: assetName,
              source: readFileSync(resolve(projectRoot, assetName)),
            });
          }
        },
      },
    ],
    build: {
      rollupOptions: {
        input: Object.fromEntries(
          pageNames.map((pageName) => [pageName, resolve(projectRoot, `${pageName}.html`)]),
        ),
      },
    },
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
  },
  };
});
