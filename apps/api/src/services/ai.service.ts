import axios from 'axios';
import config from '../config/env';
import { CapsuleReconstruction } from '../types';

interface AIReconstructionRequest {
  date: string;
  title: string;
  description?: string;
}

export class AIService {
  /**
   * Reconstruir un día usando el servicio de IA
   */
  static async reconstructDay(
    data: AIReconstructionRequest
  ): Promise<CapsuleReconstruction> {
    try {
      const response = await axios.post(
        `${config.aiService.url}/api/reconstruct`,
        data,
        {
          timeout: config.aiService.timeout,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      return response.data;
    } catch (error: any) {
      console.error('Error calling AI service:', error.message);
      throw new Error('Failed to reconstruct day with AI service');
    }
  }
}
