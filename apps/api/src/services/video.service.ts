import axios from 'axios';
import { pool } from '../config/database';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000/api';

export class VideoService {
  async generateVideo(userId: string, data: any) {
    try {
      // Crear registro en BD
      const query = `
        INSERT INTO videos (user_id, title, context, status, progress, created_at)
        VALUES ($1, $2, $3, $4, $5, NOW())
        RETURNING id
      `;
      
      const result = await pool.query(query, [
        userId,
        data.title,
        data.context,
        'queued',
        0
      ]);
      
      const videoId = result.rows[0].id;
      
      // Llamar servicio IA en background (no esperar)
      this.callAIService(videoId, data);
      
      return { id: videoId, status: 'queued' };
    } catch (error) {
      console.error('Error generating video:', error);
      throw error;
    }
  }

  private async callAIService(videoId: string, data: any) {
    try {
      const response = await axios.post(`${AI_SERVICE_URL}/videos/generate`, {
        title: data.title,
        context: data.context,
        style: data.style || 'cinematic'
      });
      
      // Actualizar en BD cuando esté listo
      const updateQuery = `
        UPDATE videos 
        SET video_url = $1, status = 'completed', completed_at = NOW()
        WHERE id = $2
      `;
      
      await pool.query(updateQuery, [response.data.video_url, videoId]);
    } catch (error) {
      console.error('Error calling AI service:', error);
      
      const errorQuery = `
        UPDATE videos 
        SET status = 'failed', error = $1
        WHERE id = $2
      `;
      
      await pool.query(errorQuery, [(error as any).message, videoId]);
    }
  }

  async getStatus(videoId: string) {
    const query = `
      SELECT id, title, status, progress, video_url, error, created_at
      FROM videos
      WHERE id = $1
    `;
    
    const result = await pool.query(query, [videoId]);
    return result.rows[0];
  }

  async getByUser(userId: string) {
    const query = `
      SELECT id, title, status, progress, video_url, created_at
      FROM videos
      WHERE user_id = $1
      ORDER BY created_at DESC
    `;
    
    const result = await pool.query(query, [userId]);
    return result.rows;
  }

  async delete(videoId: string) {
    const query = `DELETE FROM videos WHERE id = $1`;
    await pool.query(query, [videoId]);
  }
}
