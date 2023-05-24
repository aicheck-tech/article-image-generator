import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

import { fileURLToPath } from 'url'
import path from 'path'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
    plugins: [svelte()],
    base: "./",
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'src'),
            "@lib": path.resolve(__dirname, 'src/lib'),
            "@assets": path.resolve(__dirname, 'src/assets'),
            "@scripts": path.resolve(__dirname, 'src/scripts'),
        },
    },
   build: {
      emptyOutDir: true,
      outDir: '../public',
      assetsDir: 'assets',
      rollupOptions: {
         input: {
            main: './index.html',
         },
         output: {
            entryFileNames: 'assets/js/[name]-[hash].js',
            chunkFileNames: 'assets/js/[name]-[hash].js',
            assetFileNames: ({ name }) => {
               if (/\.(gif|jpe?g|png|svg|ico)$/.test(name ?? '')) {
                  return 'assets/images/[name].[ext]';
               }
               else if (/\.css$/.test(name ?? '')) {
                  return 'assets/css/[name]-[hash].[ext]';
               }

               return 'assets/[name]-[hash].[ext]';
            },
         }
      }     
   }
})
