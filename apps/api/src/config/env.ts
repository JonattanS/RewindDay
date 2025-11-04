export const config = {
  port: parseInt(process.env.PORT || '3000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',
  
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    name: process.env.DB_NAME || 'rewindday',
    user: process.env.DB_USER || 'rewindday',
    password: process.env.DB_PASSWORD || '',
  },

  aiService: {
    url: process.env.AI_SERVICE_URL || 'http://localhost:8000',
    timeout: parseInt(process.env.AI_SERVICE_TIMEOUT || '60000', 10),
  },

  cors: {
    origin: process.env.CORS_ORIGIN || '*',
  },
};

export default config;
