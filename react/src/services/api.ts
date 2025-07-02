import { ApiResponse, ApiError } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export class ApiService {
  static async classifyText(text: string, model: 'gemini' | 'openai'): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_URL}/classify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, model }),
      });

      const data = await response.json();

      if (!response.ok) {
        const apiError: ApiError = {
          error: 'API Error',
          message: data.message || 'Failed to classify text',
          status: response.status,
        };
        throw apiError;
      }

      return data;
    } catch (error) {
      const apiError: ApiError = {
        error: 'API Error',
        message: error instanceof Error ? error.message : 'Unknown error occurred',
        status: (error as any)?.status,
      };
      throw apiError;
    }
  }
} 
