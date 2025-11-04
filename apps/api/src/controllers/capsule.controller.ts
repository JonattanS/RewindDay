import { Request, Response } from 'express';
import { CapsuleService } from '../services/capsule.service';

export class CapsuleController {
  /**
   * Crear una nueva cápsula
   */
  static async create(req: Request, res: Response): Promise<void> {
    try {
      const { date, title, description } = req.body;

      // Validaciones
      if (!date || !title) {
        res.status(400).json({
          success: false,
          error: 'Date and title are required',
        });
        return;
      }

      const capsule = await CapsuleService.createCapsule({
        date,
        title,
        description,
      });

      res.status(201).json(capsule);
    } catch (error: any) {
      console.error('Error creating capsule:', error);
      res.status(500).json({
        success: false,
        error: error.message || 'Internal server error',
      });
    }
  }

  /**
   * Obtener todas las cápsulas
   */
  static async getAll(req: Request, res: Response): Promise<void> {
    try {
      const capsules = await CapsuleService.getAllCapsules();
      res.json(capsules);
    } catch (error: any) {
      console.error('Error fetching capsules:', error);
      res.status(500).json({
        success: false,
        error: error.message || 'Internal server error',
      });
    }
  }

  /**
   * Obtener una cápsula por ID
   */
  static async getById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const capsule = await CapsuleService.getCapsuleById(id);

      if (!capsule) {
        res.status(404).json({
          success: false,
          error: 'Capsule not found',
        });
        return;
      }

      res.json(capsule);
    } catch (error: any) {
      console.error('Error fetching capsule:', error);
      res.status(500).json({
        success: false,
        error: error.message || 'Internal server error',
      });
    }
  }

  /**
   * Reconstruir día con IA
   */
  static async reconstruct(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;

      const capsule = await CapsuleService.reconstructDay(id);

      if (!capsule) {
        res.status(404).json({
          success: false,
          error: 'Capsule not found',
        });
        return;
      }

      res.json(capsule);
    } catch (error: any) {
      console.error('Error reconstructing capsule:', error);
      res.status(500).json({
        success: false,
        error: error.message || 'Internal server error',
      });
    }
  }

  /**
   * Eliminar una cápsula
   */
  static async delete(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;

      const deleted = await CapsuleService.deleteCapsule(id);

      if (!deleted) {
        res.status(404).json({
          success: false,
          error: 'Capsule not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Capsule deleted successfully',
      });
    } catch (error: any) {
      console.error('Error deleting capsule:', error);
      res.status(500).json({
        success: false,
        error: error.message || 'Internal server error',
      });
    }
  }
}
