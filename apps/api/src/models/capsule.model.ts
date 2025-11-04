import { v4 as uuidv4 } from 'uuid';
import pool from '../config/database';
import { Capsule, CreateCapsuleDTO, CapsuleReconstruction } from '../types';

export class CapsuleModel {
  /**
   * Crear una nueva cápsula
   */
  static async create(data: CreateCapsuleDTO): Promise<Capsule> {
    const id = uuidv4();
    const query = `
      INSERT INTO capsules (id, date, title, description, status)
      VALUES ($1, $2, $3, $4, 'pending')
      RETURNING *;
    `;
    
    const values = [id, data.date, data.title, data.description || null];
    const result = await pool.query(query, values);
    
    return this.mapRow(result.rows);
  }

  /**
   * Obtener una cápsula por ID
   */
  static async findById(id: string): Promise<Capsule | null> {
    const query = 'SELECT * FROM capsules WHERE id = $1;';
    const result = await pool.query(query, [id]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return this.mapRow(result.rows);
  }

  /**
   * Obtener todas las cápsulas
   */
  static async findAll(): Promise<Capsule[]> {
    const query = 'SELECT * FROM capsules ORDER BY created_at DESC;';
    const result = await pool.query(query);
    
    return result.rows.map((row: any) => this.mapRow(row));
  }

  /**
   * Actualizar el estado de una cápsula
   */
  static async updateStatus(
    id: string,
    status: string
  ): Promise<Capsule | null> {
    const query = `
      UPDATE capsules
      SET status = $1, updated_at = CURRENT_TIMESTAMP
      WHERE id = $2
      RETURNING *;
    `;
    
    const result = await pool.query(query, [status, id]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return this.mapRow(result.rows);
  }

  /**
   * Actualizar la reconstrucción de una cápsula
   */
  static async updateReconstruction(
    id: string,
    reconstruction: CapsuleReconstruction
  ): Promise<Capsule | null> {
    const query = `
      UPDATE capsules
      SET reconstruction = $1, status = 'completed', updated_at = CURRENT_TIMESTAMP
      WHERE id = $2
      RETURNING *;
    `;
    
    const result = await pool.query(query, [
      JSON.stringify(reconstruction),
      id,
    ]);
    
    if (result.rows.length === 0) {
      return null;
    }
    
    return this.mapRow(result.rows);
  }

  /**
   * Eliminar una cápsula
   */
  static async delete(id: string): Promise<boolean> {
    const query = 'DELETE FROM capsules WHERE id = $1;';
    const result = await pool.query(query, [id]);
    
    return result.rowCount !== null && result.rowCount > 0;
  }

  /**
   * Mapear fila de base de datos a objeto Capsule
   */
  private static mapRow(row: any): Capsule {
    return {
      id: row.id,
      date: row.date,
      title: row.title,
      description: row.description,
      status: row.status,
      reconstruction: row.reconstruction,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    };
  }
}

export default CapsuleModel;
