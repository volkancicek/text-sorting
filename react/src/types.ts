export interface Message {
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
}

export interface ApiResponse {
  result?: string;
  error?: string;
  message?: string;
}

export interface ApiError {
  error: string;
  message?: string;
} 