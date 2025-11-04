import express from 'express';
import { VideoController } from '../controllers/video.controller';

export const videoRoutes = express.Router();
const videoController = new VideoController();

// Generar video
videoRoutes.post('/videos/generate', (req, res) => videoController.generateVideo(req, res));

// Obtener estado
videoRoutes.get('/videos/:id/status', (req, res) => videoController.getStatus(req, res));

// Descargar video
videoRoutes.get('/videos/:id/download', (req, res) => videoController.downloadVideo(req, res));

// Listar videos
videoRoutes.get('/videos', (req, res) => videoController.listVideos(req, res));

// Eliminar video
videoRoutes.delete('/videos/:id', (req, res) => videoController.deleteVideo(req, res));