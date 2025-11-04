import { CapsuleModel } from '../models/capsule.model';
import { AIService } from './ai.service';
import { Capsule, CreateCapsuleDTO } from '../types';

export class CapsuleService {
  /**
   * Crear una nueva cápsula
   */
  static async createCapsule(data: CreateCapsuleDTO): Promise<Capsule> {
    return await CapsuleModel.create(data);
  }

  /**
   * Obtener todas las cápsulas
   */
  static async getAllCapsules(): Promise<Capsule[]> {
    return await CapsuleModel.findAll();
  }

  /**
   * Obtener una cápsula por ID
   */
  static async getCapsuleById(id: string): Promise<Capsule | null> {
    return await CapsuleModel.findById(id);
  }

  /**
   * Reconstruir un día usando IA
   */
  static async reconstructDay(capsuleId: string): Promise<Capsule | null> {
    // Obtener la cápsula
    const capsule = await CapsuleModel.findById(capsuleId);
    if (!capsule) {
      return null;
    }

    // Actualizar estado a "processing"
    await CapsuleModel.updateStatus(capsuleId, 'processing');

    try {
      // Llamar al servicio de IA
      const reconstruction = await AIService.reconstructDay({
        date: capsule.date,
        title: capsule.title,
        description: capsule.description,
      });

      // Actualizar la cápsula con la reconstrucción
      const updated = await CapsuleModel.updateReconstruction(
        capsuleId,
        reconstruction
      );

      return updated;
    } catch (error) {
      // Marcar como fallida en caso de error
      await CapsuleModel.updateStatus(capsuleId, 'failed');
      throw error;
    }
  }

  /**
   * Eliminar una cápsula
   */
  static async deleteCapsule(id: string): Promise<boolean> {
    return await CapsuleModel.delete(id);
  }
}
