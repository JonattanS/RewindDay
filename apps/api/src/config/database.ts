import { Pool } from 'pg';
import config from './env';

export const pool = new Pool({
  host: config.database.host,
  port: config.database.port,
  database: config.database.name,
  user: config.database.user,
  password: config.database.password,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Manejo de errores del pool
pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
  process.exit(-1);
});

/**
 * Inicializar base de datos - crear tablas si no existen
 */
export async function initDatabase() {
  const client = await pool.connect();
  
  try {
    // Crear tabla de cápsulas
    await client.query(`
      CREATE TABLE IF NOT EXISTS capsules (
        id UUID PRIMARY KEY,
        date DATE NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        reconstruction JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Crear índices
    await client.query(`
      CREATE INDEX IF NOT EXISTS idx_capsules_date ON capsules(date);
      CREATE INDEX IF NOT EXISTS idx_capsules_status ON capsules(status);
      CREATE INDEX IF NOT EXISTS idx_capsules_created_at ON capsules(created_at);
    `);

    console.log('Database tables initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
    throw error;
  } finally {
    client.release();
  }
}

export default pool;
