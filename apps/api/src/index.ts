import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import capsuleRoutes from './routes/capsule.routes';
import { errorHandler } from './middleware/errorHandler';
import { initDatabase } from './config/database';
import { videoRoutes } from './routes/video.routes';
// Cargar variables de entorno
dotenv.config();

// Agregar estas líneas:


const app = express();
app.use('/api', videoRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 API running on http://localhost:${PORT}`);
  console.log(`🎬 Videos at http://localhost:8000/api`);
});

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'RewindDay API',
    timestamp: new Date().toISOString(),
  });
});

// Routes
app.use('/api/capsules', capsuleRoutes);

// Error handler (debe ir al final)
app.use(errorHandler);

// Iniciar servidor
async function startServer() {
  try {
    // Inicializar base de datos
    await initDatabase();
    console.log('✅ Database connected and initialized');

    // Iniciar servidor
    app.listen(PORT, () => {
      console.log(`🚀 RewindDay API running on port ${PORT}`);
      console.log(`📊 Environment: ${process.env.NODE_ENV}`);
      console.log(`🔗 AI Service: ${process.env.AI_SERVICE_URL}`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

startServer();

export default app;
