//const { resolve } = require('path');
import {resolve} from 'path';
import vue from '@vitejs/plugin-vue';
import dynamicImport from 'vite-plugin-dynamic-import';
import svgLoader from 'vite-svg-loader';

module.exports = {
    plugins: [
        vue(),
        svgLoader(),
        dynamicImport()
        ],
    root: resolve('./static/src'),
    base: '/static/',
    server: {
        host: 'localhost',
        port: 3000,
        open: false,
        watch: {
            usePolling: true,
            disableGlobbing: false,
        },
    },
    resolve: {
        extensions: ['.js', '.json', '.vue'],
    },
    build: {
        outDir: resolve('./static/dist'),
        assetsDir: '',
        manifest: true,
        emptyOutDir: true,
        target: 'es2015',
        rollupOptions: {
            input: {
                main: resolve('./static/src/js/main.js'),
            },
            output: {
                chunkFileNames: './static/src/js/[name].js?id=[chunkhash]',
            },
        },
    },
};