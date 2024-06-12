import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Expose the server on the network
    port: 5173, // Ensure the port is set to 5173
    proxy: {
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
});
