// Marketplace API service - communicates with main backend server
const MARKETPLACE_API_BASE_URL = process.env.NEXT_PUBLIC_MARKETPLACE_API_URL || 'http://localhost:5000';

export interface Product {
  id: string;
  name: string;
  category: 'seeds' | 'fertilizer' | 'equipment' | 'pesticide';
  price: number;
  unit: string;
  seller: string;
  location: string;
  rating: number;
  reviews: number;
  inStock: boolean;
  image: string;
  description: string;
  priceChange: number;
}

export interface MarketPrice {
  crop: string;
  currentPrice: number;
  unit: string;
  change: number;
  changePercent: number;
  market: string;
  lastUpdated: string;
}

export interface OrderRequest {
  productId: string;
  quantity: number;
  deliveryAddress: {
    street: string;
    city: string;
    state: string;
    pincode: string;
  };
  contactInfo: {
    name: string;
    phone: string;
    email: string;
  };
}

export interface MarketInsight {
  crop: string;
  demandTrend: 'up' | 'down' | 'stable';
  priceProjection: number;
  seasonalFactor: number;
  riskLevel: 'low' | 'medium' | 'high';
  bestRegions: string[];
  optimalTiming: string;
}

export class MarketplaceService {
  private static async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${MARKETPLACE_API_BASE_URL}${endpoint}`;
    
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
      console.error('Marketplace API request failed:', error);
      throw error;
    }
  }

  // Get all products with optional filtering
  static async getProducts(filters: {
    category?: string;
    search?: string;
    location?: string;
    minPrice?: number;
    maxPrice?: number;
  } = {}): Promise<Product[]> {
    const queryParams = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        queryParams.append(key, value.toString());
      }
    });

    const endpoint = `/marketplace/products${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
    const response = await this.makeRequest<{ products: Product[] }>(endpoint);
    return response.products;
  }

  // Get current market prices
  static async getMarketPrices(): Promise<MarketPrice[]> {
    const response = await this.makeRequest<{ prices: MarketPrice[] }>('/marketplace/prices');
    return response.prices;
  }

  // Get market insights for analytics
  static async getMarketInsights(): Promise<MarketInsight[]> {
    const response = await this.makeRequest<{ insights: MarketInsight[] }>('/analytics/insights');
    return response.insights;
  }

  // Place an order
  static async placeOrder(orderRequest: OrderRequest): Promise<{ orderId: string; status: string }> {
    return this.makeRequest<{ orderId: string; status: string }>('/marketplace/orders', {
      method: 'POST',
      body: JSON.stringify(orderRequest),
    });
  }

  // Get seller contact information
  static async getSellerContact(sellerId: string): Promise<{ phone: string; email: string; verified: boolean }> {
    return this.makeRequest<{ phone: string; email: string; verified: boolean }>(`/marketplace/sellers/${sellerId}/contact`);
  }

  // Add product to favorites
  static async addToFavorites(productId: string): Promise<{ success: boolean }> {
    return this.makeRequest<{ success: boolean }>('/marketplace/favorites', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    });
  }

  // Get user's order history
  static async getOrderHistory(): Promise<Array<{
    orderId: string;
    products: Product[];
    totalAmount: number;
    status: string;
    orderDate: string;
    deliveryDate?: string;
  }>> {
    return this.makeRequest('/marketplace/orders/history');
  }

  // Search products by location
  static async searchByLocation(latitude: number, longitude: number, radius: number = 50): Promise<Product[]> {
    return this.makeRequest<Product[]>(`/marketplace/search/location?lat=${latitude}&lng=${longitude}&radius=${radius}`);
  }

  // Get price history for a specific crop
  static async getPriceHistory(crop: string, days: number = 30): Promise<Array<{
    date: string;
    price: number;
    volume: number;
  }>> {
    return this.makeRequest(`/marketplace/prices/history?crop=${crop}&days=${days}`);
  }
}

// Utility functions for marketplace
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-IN', { 
    style: 'currency', 
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(amount);
};

export const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
  const R = 6371; // Earth's radius in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
};

export const getDeliveryEstimate = (distance: number): string => {
  if (distance < 50) return '1-2 days';
  if (distance < 200) return '3-5 days';
  if (distance < 500) return '5-7 days';
  return '7-10 days';
};

export const validateOrderRequest = (order: OrderRequest): string[] => {
  const errors: string[] = [];
  
  if (!order.productId) errors.push('Product ID is required');
  if (!order.quantity || order.quantity <= 0) errors.push('Valid quantity is required');
  
  // Validate delivery address
  if (!order.deliveryAddress.street) errors.push('Street address is required');
  if (!order.deliveryAddress.city) errors.push('City is required');
  if (!order.deliveryAddress.state) errors.push('State is required');
  if (!order.deliveryAddress.pincode || !/^\d{6}$/.test(order.deliveryAddress.pincode)) {
    errors.push('Valid 6-digit pincode is required');
  }
  
  // Validate contact info
  if (!order.contactInfo.name) errors.push('Name is required');
  if (!order.contactInfo.phone || !/^\d{10}$/.test(order.contactInfo.phone)) {
    errors.push('Valid 10-digit phone number is required');
  }
  if (!order.contactInfo.email || !/\S+@\S+\.\S+/.test(order.contactInfo.email)) {
    errors.push('Valid email address is required');
  }
  
  return errors;
};
