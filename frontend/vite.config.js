import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 3000,
    watch: {
      // Indispensable : Docker ne transmet pas toujours les événements de fichiers
      // au système d'exploitation hôte sans le polling.
      usePolling: true,
      interval: 100,
    },
    proxy: {
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
  },
});
