/**
 * Disease Detection API Service
 * Direct connection to the FastAPI disease detection server
 */

export interface DiseaseDetectionResult {
  predicted_class: string;
  crop: string;
  confidence: number;
  risk_assessment: {
    overall_risk: string;
    risk_factors: string[];
    recommendations: string[];
  };
  disease_info: {
    description?: string;
    symptoms?: string[];
    solutions?: string[];
    prevention?: string[];
  };
  explanation?: {
    heatmap_available: boolean;
    attention_regions: number[][];
    explanation_image?: string; // Base64 encoded Grad-CAM overlay
    error?: string;
  };
  class_probabilities: Record<string, number>;
  timestamp: string;
}

export interface DiseaseApiResponse {
  predicted_class: string;
  crop: string;
  confidence: number;
  risk_assessment: {
    overall_risk?: string;
    risk_factors?: string[];
    recommendations?: string[];
  };
  disease_info: {
    description?: string;
    symptoms?: string[];
    solutions?: string[];
    prevention?: string[];
  };
  explanation?: {
    explanation_image?: string;
    error?: string;
    predicted_class?: string;
    confidence?: number;
    save_path?: string;
  };
  class_probabilities: Record<string, number>;
}

class DiseaseDetectionApi {
  private baseUrl: string;
  private timeout: number;

  constructor() {
    // Use environment variable or default to localhost
    this.baseUrl = process.env.NEXT_PUBLIC_DISEASE_API_URL || 'http://localhost:8001';
    this.timeout = 30000; // 30 seconds
  }

  /**
   * Check if the disease detection service is available
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000) // 5 second timeout for health check
      });
      
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }
      
      const data = await response.json();
      return data.status === 'ok' && data.model_loaded;
    } catch (error) {
      console.error('Disease API health check failed:', error);
      return false;
    }
  }

  /**
   * Detect disease from an image file
   */
  async detectDisease(
    imageFile: File,
    options: {
      includeExplanation?: boolean;
      weatherHumidity?: number;
      weatherTemperature?: number;
      weatherRainfall?: number;
      growthStage?: string;
    } = {}
  ): Promise<DiseaseDetectionResult> {
    try {
      // Validate image file
      this.validateImageFile(imageFile);

      // Create FormData for multipart upload
      const formData = new FormData();
      formData.append('file', imageFile);
      
      // Add optional parameters
      if (options.includeExplanation !== undefined) {
        formData.append('include_explanation', options.includeExplanation.toString());
      }
      if (options.weatherHumidity !== undefined) {
        formData.append('weather_humidity', options.weatherHumidity.toString());
      }
      if (options.weatherTemperature !== undefined) {
        formData.append('weather_temperature', options.weatherTemperature.toString());
      }
      if (options.weatherRainfall !== undefined) {
        formData.append('weather_rainfall', options.weatherRainfall.toString());
      }
      if (options.growthStage) {
        formData.append('growth_stage', options.growthStage);
      }

      const response = await fetch(`${this.baseUrl}/predict`, {
        method: 'POST',
        body: formData,
        signal: AbortSignal.timeout(this.timeout)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API request failed: ${response.status}`);
      }

      const data: DiseaseApiResponse = await response.json();
      return this.formatResponse(data);

    } catch (error) {
      console.error('Disease detection error:', error);
      
      if (error instanceof Error) {
        if (error.name === 'TimeoutError') {
          throw new Error('Request timeout. The AI server might be busy.');
        }
        throw error;
      }
      
      throw new Error('Unexpected error during disease detection');
    }
  }

  /**
   * Get list of supported disease classes
   */
  async getDiseaseClasses(): Promise<string[]> {
    try {
      const response = await fetch(`${this.baseUrl}/classes`, {
        method: 'GET',
        signal: AbortSignal.timeout(10000)
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch classes: ${response.status}`);
      }

      const data = await response.json();
      return data.classes || [];
    } catch (error) {
      console.error('Error fetching disease classes:', error);
      throw new Error('Failed to fetch supported disease classes');
    }
  }

  /**
   * Get detailed information about a specific disease
   */
  async getDiseaseInfo(crop: string, disease: string): Promise<{
    description?: string;
    symptoms?: string[];
    solutions?: string[];
    prevention?: string[];
  }> {
    try {
      const response = await fetch(`${this.baseUrl}/disease_info/${crop}/${disease}`, {
        method: 'GET',
        signal: AbortSignal.timeout(10000)
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch disease info: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching disease info:', error);
      throw new Error('Failed to fetch disease information');
    }
  }

  /**
   * Process multiple images in batch
   */
  async batchDetectDisease(imageFiles: File[]): Promise<DiseaseDetectionResult[]> {
    try {
      if (imageFiles.length === 0) {
        throw new Error('No images provided');
      }

      if (imageFiles.length > 10) {
        throw new Error('Maximum 10 images allowed per batch');
      }

      // Validate all images
      imageFiles.forEach(file => this.validateImageFile(file));

      const formData = new FormData();
      imageFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch(`${this.baseUrl}/batch_predict`, {
        method: 'POST',
        body: formData,
        signal: AbortSignal.timeout(this.timeout * 2) // Double timeout for batch
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Batch prediction failed: ${response.status}`);
      }

      const data: DiseaseApiResponse[] = await response.json();
      return data.map(result => this.formatResponse(result));

    } catch (error) {
      console.error('Batch disease detection error:', error);
      throw error;
    }
  }

  /**
   * Validate image file before upload
   */
  private validateImageFile(file: File): void {
    // Check file type
    if (!file.type.startsWith('image/')) {
      throw new Error('Please select a valid image file');
    }

    // Check file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      throw new Error('Image size must be less than 10MB');
    }

    // Check supported formats
    const supportedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'];
    if (!supportedTypes.includes(file.type)) {
      throw new Error('Supported formats: JPEG, PNG, BMP, TIFF');
    }
  }

  /**
   * Format API response to match frontend interface
   */
  private formatResponse(data: DiseaseApiResponse): DiseaseDetectionResult {
    return {
      predicted_class: data.predicted_class,
      crop: data.crop || 'Unknown',
      confidence: data.confidence || 0,
      risk_assessment: {
        overall_risk: data.risk_assessment?.overall_risk || 'Low',
        risk_factors: data.risk_assessment?.risk_factors || [],
        recommendations: data.risk_assessment?.recommendations || []
      },
      disease_info: {
        description: data.disease_info?.description,
        symptoms: this.extractArray(data.disease_info?.symptoms),
        solutions: this.extractArray(data.disease_info?.solutions),
        prevention: this.extractArray(data.disease_info?.prevention)
      },
      explanation: data.explanation ? {
        heatmap_available: !!data.explanation.explanation_image,
        attention_regions: [], // This would come from the API if available
        explanation_image: data.explanation.explanation_image || '',
        error: data.explanation.error
      } : undefined,
      class_probabilities: data.class_probabilities || {},
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Format disease name for display
   */
  private formatDiseaseName(className: string): string {
    return className
      .replace(/___/g, ' - ')
      .replace(/__/g, ' - ')
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  }

  /**
   * Map risk level to severity
   */
  private mapRiskToSeverity(risk: string): 'Low' | 'Medium' | 'High' {
    const riskLower = risk.toLowerCase();
    if (riskLower.includes('high') || riskLower.includes('critical')) {
      return 'High';
    }
    if (riskLower.includes('medium') || riskLower.includes('moderate')) {
      return 'Medium';
    }
    return 'Low';
  }

  /**
   * Extract array from various input formats
   */
  private extractArray(input: unknown): string[] {
    if (Array.isArray(input)) {
      return input;
    }
    if (typeof input === 'string') {
      return input.split('\n').filter(line => line.trim());
    }
    return [];
  }
}

// Export singleton instance
export const diseaseApi = new DiseaseDetectionApi();

// Export utility functions
export const formatDiseaseName = (className: string): string => {
  return className
    .replace(/___/g, ' - ')
    .replace(/__/g, ' - ')
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

export const getSeverityColor = (severity: string): string => {
  switch (severity.toLowerCase()) {
    case 'high':
      return 'bg-red-100 text-red-800 border-red-200';
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case 'low':
      return 'bg-green-100 text-green-800 border-green-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
};

export const getRiskIcon = (severity: string): string => {
  switch (severity.toLowerCase()) {
    case 'high':
      return '🔴';
    case 'medium':
      return '🟡';
    case 'low':
      return '🟢';
    default:
      return '⚪';
  }
};