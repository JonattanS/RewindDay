import axios, { AxiosInstance } from 'axios';
import API_URL from '../config/api';

interface VideoGenerationRequest {
  title: string;
  context: string;
  style?: 'professional' | 'cinematic' | 'documentary';
}

interface VideoStatus {
  id: string;
  status: 'queued' | 'generating' | 'completed' | 'failed';
  progress: number;
  message: string;
}

export class VideoService {
  private api: AxiosInstance;

  constructor() {
    if (typeof API_URL === 'string') {
      this.api = axios.create({
        baseURL: API_URL,
        timeout: 60000,
      });
    } else {
      // If the config exports an Axios instance, use it directly
      this.api = API_URL as AxiosInstance;
    }
  }

  async generateVideo(request: VideoGenerationRequest) {
    try {
      const response = await this.api.post('/api/videos/generate', request);
      return response.data;
    } catch (error) {
      console.error('Error generating video:', error);
      throw error;
    }
  }

  async getVideoStatus(videoId: string): Promise<VideoStatus> {
    try {
      const response = await this.api.get(`/api/videos/${videoId}/status`);
      return response.data;
    } catch (error) {
      console.error('Error getting status:', error);
      throw error;
    }
  }

  async downloadVideo(videoId: string) {
    return `${API_URL}/api/videos/${videoId}/download`;
  }

  async deleteVideo(videoId: string) {
    try {
      await this.api.delete(`/api/videos/${videoId}`);
    } catch (error) {
      console.error('Error deleting video:', error);
      throw error;
    }
  }

  async listVideos() {
    try {
      const response = await this.api.get('/api/videos');
      return response.data;
    } catch (error) {
      console.error('Error listing videos:', error);
      throw error;
    }
  }
}

export const videoService = new VideoService();
