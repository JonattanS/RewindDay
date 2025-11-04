export interface Capsule {
  id: string;
  date: string;
  title: string;
  description?: string;
  status: CapsuleStatus;
  reconstruction?: CapsuleReconstruction;
  createdAt: string;
  updatedAt: string;
}

export type CapsuleStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface CapsuleReconstruction {
  summary: string;
  highlights: string[];
  mood: string;
  weather?: string;
  events: ReconstructedEvent[];
  aiInsights: string;
  generatedAt: string;
}

export interface ReconstructedEvent {
  time: string;
  description: string;
  category: string;
  importance: number;
}

export interface CreateCapsuleDTO {
  date: string;
  title: string;
  description?: string;
  additionalData?: any;
}

export interface AIReconstructionRequest {
  date: string;
  title: string;
  description?: string;
}

export interface AIReconstructionResponse {
  success: boolean;
  data?: CapsuleReconstruction;
  error?: string;
}
