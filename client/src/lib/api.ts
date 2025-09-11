// API service for communicating with the AI backend for crop recommendations
const AI_API_BASE_URL = '/api';

export interface CropPredictionRequest {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
  area_ha?: number;
  previous_crop?: string;
  season?: string;
  region?: string;
  planting_date?: string;
}

export interface FertilizerRecommendation {
  type: string;
  dosage_kg_per_ha: number;
  cost: number;
}

export interface ProfitBreakdown {
  gross: number;
  investment: number;
  net: number;
  roi: number;
}

export interface PreviousCropAnalysis {
  previous_crop: string;
  original_npk: [number, number, number];
  adjusted_npk: [number, number, number];
  nutrient_impact: string;
}

export interface SeasonAnalysis {
  detected_season: string;
  season_suitability: string;
  season_explanation: string;
}

export interface CropPredictionResponse {
  recommended_crop: string;
  confidence: number;
  why: string[];
  expected_yield_t_per_acre: number;
  yield_interval_p10_p90: [number, number];
  profit_breakdown: ProfitBreakdown;
  fertilizer_recommendation: FertilizerRecommendation;
  previous_crop_analysis: PreviousCropAnalysis;
  season_analysis: SeasonAnalysis;
  model_version: string;
  timestamp: string;
  area_analyzed_ha: number;
  region: string;
}

export class CropAIService {
  private static async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${AI_API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error('AI API request failed:', error);
      throw error;
    }
  }

  static async getCropRecommendation(
    data: CropPredictionRequest
  ): Promise<CropPredictionResponse> {
    return this.makeRequest<CropPredictionResponse>('/predict', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  static async healthCheck(): Promise<{ status: string; message: string }> {
    return this.makeRequest<{ status: string; message: string }>('/health');
  }

  static async getApiInfo(): Promise<Record<string, unknown>> {
    return this.makeRequest<Record<string, unknown>>('/');
  }
}

// Validation helpers
export const validateSoilData = (data: Partial<CropPredictionRequest>): string[] => {
  const errors: string[] = [];

  const requiredFields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'];
  
  requiredFields.forEach(field => {
    if (data[field as keyof CropPredictionRequest] === undefined || data[field as keyof CropPredictionRequest] === null) {
      errors.push(`${field} is required`);
    }
  });

  // Validate ranges
  const validations = {
    N: { min: 0, max: 200, name: 'Nitrogen' },
    P: { min: 0, max: 150, name: 'Phosphorus' },
    K: { min: 0, max: 200, name: 'Potassium' },
    temperature: { min: -10, max: 55, name: 'Temperature' },
    humidity: { min: 0, max: 100, name: 'Humidity' },
    ph: { min: 3.5, max: 9.0, name: 'pH' },
    rainfall: { min: 0, max: 5000, name: 'Rainfall' },
  };

  Object.entries(validations).forEach(([field, { min, max, name }]) => {
    const value = data[field as keyof CropPredictionRequest] as number;
    if (value !== undefined && (value < min || value > max)) {
      errors.push(`${name} must be between ${min} and ${max}`);
    }
  });

  return errors;
};

// Format utilities
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatNumber = (num: number, decimals: number = 2): string => {
  return new Intl.NumberFormat('en-IN', {
    maximumFractionDigits: decimals,
  }).format(num);
};
