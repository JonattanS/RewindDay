export interface Capsule {
  id: string;
  date: string;
  title: string;
  description?: string;
  reconstruction: CapsuleReconstruction | null;
  createdAt: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

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

export interface CreateCapsuleRequest {
  date: string;
  title: string;
  description?: string;
  additionalData?: any;
}

export interface CapsuleResponse {
  success: boolean;
  data?: Capsule;
  error?: string;
}
