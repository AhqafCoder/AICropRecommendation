// Analytics API service - communicates with main backend server
const ANALYTICS_API_BASE_URL = process.env.NEXT_PUBLIC_MARKETPLACE_API_URL || 'http://localhost:5000';

export interface WeatherForecast {
  region: string;
  temperature: {
    min: number;
    max: number;
    avg: number;
  };
  rainfall: number;
  humidity: number;
  outlook: 'favorable' | 'moderate' | 'challenging';
  impact: string;
  windSpeed: number;
  uvIndex: number;
}

export interface ProfitabilityInsight {
  crop: string;
  investmentPerAcre: number;
  expectedRevenuePerAcre: number;
  profitMargin: number;
  paybackPeriod: string;
  riskFactor: number;
  marketDemand: string;
}

export interface MarketTrend {
  crop: string;
  trend: 'up' | 'down' | 'stable';
  currentPrice: number;
  projectedPrice: number;
  confidence: number;
  timeFrame: string;
}

export interface RegionalAnalysis {
  region: string;
  cropSuitability: {
    crop: string;
    suitabilityScore: number;
    reasons: string[];
  }[];
  climateFactors: {
    temperature: number;
    rainfall: number;
    soilType: string;
  };
  marketAccess: number;
}

export class AnalyticsService {
  private static async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${ANALYTICS_API_BASE_URL}${endpoint}`;
    
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
      console.error('Analytics API request failed:', error);
      throw error;
    }
  }

  // Get weather forecast for a region
  static async getWeatherForecast(region?: string): Promise<WeatherForecast[]> {
    const response = await this.makeRequest<{ forecasts: WeatherForecast[] }>('/analytics/weather');
    return response.forecasts;
  }

  // Get profitability insights for crops
  static async getProfitabilityInsights(): Promise<ProfitabilityInsight[]> {
    const response = await this.makeRequest<{ analysis: ProfitabilityInsight[] }>('/analytics/profitability');
    return response.analysis;
  }

  // Get market trends analysis
  static async getMarketTrends(timeFrame: string = '30d'): Promise<MarketTrend[]> {
    // For now, return market insights as trends since the backend provides this data
    const response = await this.makeRequest<{ insights: any[] }>('/analytics/insights');
    return response.insights.map((insight: any) => ({
      crop: insight.crop,
      trend: insight.demandTrend,
      currentPrice: insight.currentPrice,
      projectedPrice: insight.projectedPrice,
      confidence: insight.confidence,
      timeFrame: '30d'
    }));
  }

  // Get regional crop analysis
  static async getRegionalAnalysis(region: string): Promise<RegionalAnalysis> {
    return this.makeRequest<RegionalAnalysis>(`/api/analytics/regional?region=${encodeURIComponent(region)}`);
  }

  // Get comprehensive market overview
  static async getMarketOverview(): Promise<{
    totalProducts: number;
    activeUsers: number;
    totalTransactions: number;
    growthRate: number;
    topCategories: { category: string; count: number }[];
    recentActivity: { activity: string; timestamp: string }[];
  }> {
    return this.makeRequest('/api/analytics/overview');
  }

  // Get crop performance analytics
  static async getCropPerformance(crop: string, region?: string): Promise<{
    crop: string;
    region?: string;
    averageYield: number;
    yieldTrend: 'increasing' | 'decreasing' | 'stable';
    profitMargin: number;
    marketDemand: 'high' | 'medium' | 'low';
    seasonalPattern: { month: string; demand: number }[];
    competitionLevel: 'low' | 'medium' | 'high';
  }> {
    const queryParams = new URLSearchParams({ crop });
    if (region) queryParams.append('region', region);
    
    return this.makeRequest(`/api/analytics/crop-performance?${queryParams.toString()}`);
  }

  // Get price predictions
  static async getPricePredictions(crop: string, horizon: number = 30): Promise<{
    crop: string;
    currentPrice: number;
    predictions: { date: string; price: number; confidence: number }[];
    factors: string[];
    accuracy: number;
  }> {
    return this.makeRequest(`/api/analytics/price-predictions?crop=${encodeURIComponent(crop)}&horizon=${horizon}`);
  }
}

// Utility functions for analytics
export const formatTrend = (trend: 'up' | 'down' | 'stable'): string => {
  const trendMap = {
    up: '📈 Increasing',
    down: '📉 Decreasing',
    stable: '➡️ Stable'
  };
  return trendMap[trend];
};

export const formatRiskLevel = (risk: number): { level: string; color: string } => {
  if (risk <= 0.3) return { level: 'Low Risk', color: 'green' };
  if (risk <= 0.6) return { level: 'Medium Risk', color: 'yellow' };
  return { level: 'High Risk', color: 'red' };
};

export const formatConfidence = (confidence: number): string => {
  if (confidence >= 0.8) return 'High Confidence';
  if (confidence >= 0.6) return 'Medium Confidence';
  return 'Low Confidence';
};

export const calculateROI = (investment: number, revenue: number): number => {
  return ((revenue - investment) / investment) * 100;
};

export const formatPercentage = (value: number): string => {
  return new Intl.NumberFormat('en-IN', {
    style: 'percent',
    maximumFractionDigits: 1,
  }).format(value / 100);
};
