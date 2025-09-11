import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig(({ mode }) => {
  const isProduction = mode === 'production';
  
  return {
    plugins: [react()],
    base: isProduction ? '/static' : '/',
    publicDir: 'public',
    build: {
      outDir: 'dist',
      emptyOutDir: true,
      assetsDir: 'assets',
      rollupOptions: {
        input: {
          main: resolve(__dirname, 'index.html'),
        },
        output: {
          // Keep the favicon in the root of the static directory
          assetFileNames: (assetInfo) => {
            // The asset name is in the first element of the names array
            const assetName = assetInfo.names?.[0] || '';
            if (assetName.endsWith('favicon.ico')) {
              return 'favicon.ico';
            }
            return 'assets/[name]-[hash][extname]';
          },
          entryFileNames: 'assets/[name]-[hash].js',
          chunkFileNames: 'assets/[name]-[hash].js',
        }
      },
      // This ensures all asset URLs are prefixed with /static
      manifest: true,
      // This will make sure all asset URLs are absolute
      assetsInlineLimit: 0,
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  };
});
