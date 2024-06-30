import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Expose the server on the network
    port: 5173, // Ensure the port is set to 5173
    proxy: {
      '/ws': {
        target: 'ws://ec2-3-16-217-246.us-east-2.compute.amazonaws.com:8000', //
        // target: 'ws://localhost:5173/',//    
        ws: true
      }
    }
  }
});
