import api from '../config/api';
import { 
  Capsule, 
  CreateCapsuleRequest, 
  CapsuleResponse 
} from '../types/capsule.types';

export class CapsuleService {
  /**
   * Crear una nueva cápsula del tiempo
   */
  static async createCapsule(data: CreateCapsuleRequest): Promise<CapsuleResponse> {
    try {
      const response = await api.post<Capsule>('/api/capsules', data);
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to create capsule',
      };
    }
  }

  /**
   * Reconstruir un día usando IA
   */
  static async reconstructDay(capsuleId: string): Promise<CapsuleResponse> {
    try {
      const response = await api.post<Capsule>(
        `/api/capsules/${capsuleId}/reconstruct`
      );
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to reconstruct day',
      };
    }
  }

  /**
   * Obtener una cápsula por ID
   */
  static async getCapsule(capsuleId: string): Promise<CapsuleResponse> {
    try {
      const response = await api.get<Capsule>(`/api/capsules/${capsuleId}`);
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch capsule',
      };
    }
  }

  /**
   * Obtener todas las cápsulas del usuario
   */
  static async getAllCapsules(): Promise<{
    success: boolean;
    data?: Capsule[];
    error?: string;
  }> {
    try {
      const response = await api.get<Capsule[]>('/api/capsules');
      return {
        success: true,
        data: response.data,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to fetch capsules',
      };
    }
  }

  /**
   * Eliminar una cápsula
   */
  static async deleteCapsule(capsuleId: string): Promise<{ success: boolean; error?: string }> {
    try {
      await api.delete(`/api/capsules/${capsuleId}`);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Failed to delete capsule',
      };
    }
  }
}

export default CapsuleService;
