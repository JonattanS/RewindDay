import { Router } from 'express';
import { CapsuleController } from '../controllers/capsule.controller';

const router = Router();

// POST /api/capsules - Crear nueva cápsula
router.post('/', CapsuleController.create);

// GET /api/capsules - Obtener todas las cápsulas
router.get('/', CapsuleController.getAll);

// GET /api/capsules/:id - Obtener una cápsula por ID
router.get('/:id', CapsuleController.getById);

// POST /api/capsules/:id/reconstruct - Reconstruir día con IA
router.post('/:id/reconstruct', CapsuleController.reconstruct);

// DELETE /api/capsules/:id - Eliminar cápsula
router.delete('/:id', CapsuleController.delete);

export default router;
