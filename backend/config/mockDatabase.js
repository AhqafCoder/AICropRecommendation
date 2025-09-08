// Mock database for development without PostgreSQL
const mockData = {
  products: [
    {
      id: '1',
      name: 'Premium Rice Seeds (IR64)',
      category: 'seeds',
      price: 120,
      unit: 'kg',
      seller_name: 'Green Valley Seeds',
      location: 'Punjab, India',
      product_rating: 4.8,
      review_count: 156,
      in_stock: true,
      image_url: '🌾',
      description: 'High-yield IR64 rice variety suitable for kharif season',
      price_change: -2.5
    },
    {
      id: '2',
      name: 'NPK Fertilizer (20:20:0)',
      category: 'fertilizer',
      price: 850,
      unit: '50kg bag',
      seller_name: 'FarmTech Solutions',
      location: 'Maharashtra, India',
      product_rating: 4.6,
      review_count: 89,
      in_stock: true,
      image_url: '🌱',
      description: 'Balanced NPK fertilizer for optimal crop growth',
      price_change: 3.2
    },
    {
      id: '3',
      name: 'Solar Water Pump',
      category: 'equipment',
      price: 45000,
      unit: 'unit',
      seller_name: 'AgriTech India',
      location: 'Gujarat, India',
      product_rating: 4.9,
      review_count: 34,
      in_stock: true,
      image_url: '⚡',
      description: '5HP solar-powered water pump with 2-year warranty',
      price_change: -1.8
    },
    {
      id: '4',
      name: 'Organic Pesticide',
      category: 'pesticide',
      price: 320,
      unit: 'liter',
      seller_name: 'Bio Solutions',
      location: 'Karnataka, India',
      product_rating: 4.7,
      review_count: 78,
      in_stock: false,
      image_url: '🛡️',
      description: 'Eco-friendly organic pesticide for crop protection',
      price_change: 0.5
    }
  ],
  
  marketPrices: [
    {
      crop_name: 'Rice',
      current_price: 2100,
      unit: 'quintal',
      price_change: 50,
      change_percent: 2.4,
      market_name: 'Delhi Mandi',
      last_updated: new Date()
    },
    {
      crop_name: 'Wheat',
      current_price: 2050,
      unit: 'quintal',
      price_change: -30,
      change_percent: -1.4,
      market_name: 'Punjab Mandi',
      last_updated: new Date()
    },
    {
      crop_name: 'Cotton',
      current_price: 5800,
      unit: 'quintal',
      price_change: 120,
      change_percent: 2.1,
      market_name: 'Gujarat Mandi',
      last_updated: new Date()
    }
  ],
  
  marketInsights: [
    {
      crop_name: 'Rice',
      demand_trend: 'up',
      current_price: 2100,
      projected_price: 2250,
      seasonal_factor: 1.15,
      risk_level: 'low',
      best_regions: ['Punjab', 'Haryana', 'West Bengal'],
      optimal_timing: 'June - July',
      market_share: 35.2
    },
    {
      crop_name: 'Cotton',
      demand_trend: 'up',
      current_price: 5800,
      projected_price: 6200,
      seasonal_factor: 1.25,
      risk_level: 'medium',
      best_regions: ['Gujarat', 'Maharashtra', 'Andhra Pradesh'],
      optimal_timing: 'May - June',
      market_share: 28.7
    }
  ]
};

// Mock database query function
const query = async (queryString, params = []) => {
  console.log('Mock DB Query:', queryString.substring(0, 50) + '...');
  
  // Simulate database operations based on query
  if (queryString.includes('SELECT') && queryString.includes('products')) {
    return { rows: mockData.products };
  }
  
  if (queryString.includes('market_prices')) {
    return { rows: mockData.marketPrices };
  }
  
  if (queryString.includes('market_insights')) {
    return { rows: mockData.marketInsights };
  }
  
  if (queryString.includes('INSERT INTO orders')) {
    return { rows: [{ id: Math.floor(Math.random() * 1000) }] };
  }
  
  if (queryString.includes('INSERT INTO crop_predictions')) {
    return { rows: [{ id: Math.floor(Math.random() * 1000) }] };
  }
  
  // Default empty result
  return { rows: [] };
};

// Mock transaction function
const transaction = async (callback) => {
  const mockClient = { query };
  return await callback(mockClient);
};

// Mock test connection
const testConnection = async () => {
  console.log('✅ Mock database connected successfully');
  return true;
};

module.exports = {
  query,
  transaction,
  testConnection
};
