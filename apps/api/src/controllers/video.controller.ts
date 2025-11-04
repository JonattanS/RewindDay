import { Request, Response } from 'express';
import axios from 'axios';

const AI_SERVICE_URL = 'http://localhost:8000/api';

export class VideoController {
  
  async generateVideo(req: Request, res: Response) {
    try {
      const { title, context, style } = req.body;
      
      // Validar
      if (!title || !context) {
        return res.status(400).json({ error: 'Title and context required' });
      }
      
      // Llamar servicio IA
      const response = await axios.post(`${AI_SERVICE_URL}/videos/generate`, {
        title,
        context,
        style: style || 'cinematic'
      });
      
      return res.json(response.data);
      
    } catch (error: any) {
      console.error('Error:', error);
      return res.status(500).json({ error: error.message });
    }
  }
  
  async getStatus(req: Request, res: Response) {
    try {
      const { id } = req.params;
      
      const response = await axios.get(`${AI_SERVICE_URL}/videos/${id}/status`);
      
      return res.json(response.data);
      
    } catch (error: any) {
      return res.status(500).json({ error: error.message });
    }
  }
  
  async downloadVideo(req: Request, res: Response) {
    try {
      const { id } = req.params;
      
      // Redirigir a IA service
      const response = await axios.get(`${AI_SERVICE_URL}/videos/${id}/download`, {
        responseType: 'stream'
      });
      
      res.setHeader('Content-Type', 'video/mp4');
      res.setHeader('Content-Disposition', `attachment; filename="${id}.mp4"`);
      
      response.data.pipe(res);
      
    } catch (error: any) {
      return res.status(500).json({ error: error.message });
    }
  }
  
  async listVideos(req: Request, res: Response) {
    try {
      const response = await axios.get(`${AI_SERVICE_URL}/videos`);
      return res.json(response.data);
      
    } catch (error: any) {
      return res.status(500).json({ error: error.message });
    }
  }
  
  async deleteVideo(req: Request, res: Response) {
    try {
      const { id } = req.params;
      
      const response = await axios.delete(`${AI_SERVICE_URL}/videos/${id}`);
      
      return res.json(response.data);
      
    } catch (error: any) {
      return res.status(500).json({ error: error.message });
    }
  }
}
