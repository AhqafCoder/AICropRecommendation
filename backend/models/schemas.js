// Data models and validation schemas for CropAI Backend

const Joi = require('joi');

// Product Schema
const productSchema = Joi.object({
  id: Joi.string().optional(),
  name: Joi.string().required().min(1).max(100),
  category: Joi.string().valid('seeds', 'fertilizer', 'equipment', 'pesticide').required(),
  price: Joi.number().positive().required(),
  unit: Joi.string().required(),
  seller: Joi.string().required(),
  location: Joi.string().required(),
  rating: Joi.number().min(0).max(5).default(0),
  reviews: Joi.number().integer().min(0).default(0),
  inStock: Joi.boolean().default(true),
  image: Joi.string().uri().optional(),
  description: Joi.string().max(500).optional(),
  priceChange: Joi.number().optional(),
  sellerId: Joi.string().optional(),
  dateAdded: Joi.date().default(Date.now)
});

// Analytics Data Schema
const analyticsSchema = Joi.object({
  period: Joi.string().valid('day', 'week', 'month', 'year').default('month'),
  cropType: Joi.string().optional(),
  location: Joi.string().optional()
});

// Dashboard Stats Schema
const dashboardStatsSchema = Joi.object({
  totalRevenue: Joi.number().default(0),
  totalCrops: Joi.number().integer().default(0),
  healthyCrops: Joi.number().min(0).max(100).default(0),
  diseaseAlerts: Joi.number().integer().min(0).default(0)
});

// Market Insight Schema
const marketInsightSchema = Joi.object({
  crop: Joi.string().required(),
  currentPrice: Joi.number().positive().required(),
  priceChange: Joi.number().required(),
  demandTrend: Joi.string().valid('up', 'down', 'stable').required(),
  recommendedAction: Joi.string().required(),
  confidence: Joi.number().min(0).max(100).required()
});

// Sample Data Generators
class DataGenerator {
  static generateProducts(count = 50) {
    const categories = ['seeds', 'fertilizer', 'equipment', 'pesticide'];
    const locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad'];
    const products = [];

    const productNames = {
      seeds: ['Wheat Seeds', 'Rice Seeds', 'Corn Seeds', 'Tomato Seeds', 'Potato Seeds'],
      fertilizer: ['NPK Fertilizer', 'Organic Compost', 'Urea', 'Phosphate', 'Potash'],
      equipment: ['Tractor', 'Harvester', 'Plow', 'Irrigation System', 'Sprayer'],
      pesticide: ['Insecticide', 'Herbicide', 'Fungicide', 'Organic Pesticide', 'Bio-Pesticide']
    };

    for (let i = 0; i < count; i++) {
      const category = categories[Math.floor(Math.random() * categories.length)];
      const names = productNames[category];
      const name = names[Math.floor(Math.random() * names.length)];
      
      products.push({
        id: `prod_${i + 1}`,
        name: `${name} Premium`,
        category,
        price: Math.floor(Math.random() * 5000) + 100,
        unit: category === 'equipment' ? 'piece' : 'kg',
        seller: `Seller ${i + 1}`,
        location: locations[Math.floor(Math.random() * locations.length)],
        rating: Math.round((Math.random() * 2 + 3) * 10) / 10,
        reviews: Math.floor(Math.random() * 100) + 1,
        inStock: Math.random() > 0.1,
        image: `https://picsum.photos/300/200?random=${i}`,
        description: `High quality ${name.toLowerCase()} for your farming needs`,
        priceChange: Math.round((Math.random() * 20 - 10) * 10) / 10,
        sellerId: `seller_${i + 1}`,
        dateAdded: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
      });
    }

    return products;
  }

  static generateAnalytics() {
    return {
      cropYield: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        data: [2400, 2100, 2800, 3200, 2900, 3400]
      },
      revenue: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        data: [125000, 134000, 145000, 167000, 156000, 189000]
      },
      cropHealth: {
        healthy: 87.5,
        diseased: 8.2,
        pending: 4.3
      },
      monthlyStats: {
        totalRevenue: 1250000,
        totalCrops: 2340,
        healthyCrops: 87.5,
        diseaseAlerts: 12
      }
    };
  }

  static generateDashboardStats() {
    return {
      totalRevenue: 1250670,
      totalCrops: 2340,
      healthyCrops: 87.5,
      diseaseAlerts: 12,
      recentActivity: [
        {
          id: 1,
          type: 'sale',
          message: 'Sold 500kg of wheat at ₹25/kg',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          amount: 12500
        },
        {
          id: 2,
          type: 'alert',
          message: 'Disease detected in tomato crop - Block A',
          timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
          severity: 'medium'
        },
        {
          id: 3,
          type: 'harvest',
          message: 'Harvested 2 tons of rice from Field B',
          timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
          quantity: 2000
        }
      ]
    };
  }

  static generateMarketInsights() {
    const crops = ['Wheat', 'Rice', 'Corn', 'Tomato', 'Potato', 'Soybean'];
    return crops.map(crop => ({
      crop,
      currentPrice: Math.floor(Math.random() * 50) + 20,
      priceChange: Math.round((Math.random() * 20 - 10) * 10) / 10,
      demandTrend: ['up', 'down', 'stable'][Math.floor(Math.random() * 3)],
      recommendedAction: ['Hold', 'Sell', 'Buy More'][Math.floor(Math.random() * 3)],
      confidence: Math.floor(Math.random() * 30) + 70
    }));
  }
}

module.exports = {
  productSchema,
  analyticsSchema,
  dashboardStatsSchema,
  marketInsightSchema,
  DataGenerator
};