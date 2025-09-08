require('dotenv').config();
const db = require('../config/database');

// Seed sample data for testing
const seedData = async () => {
  try {
    console.log('🌱 Seeding sample data...');

    // Sample sellers
    const sellersData = [
      ['Green Valley Seeds', 'contact@greenvalley.com', '9876543210', 'Punjab, India', 4.8, true],
      ['FarmTech Solutions', 'info@farmtech.com', '9876543211', 'Maharashtra, India', 4.6, true],
      ['AgriTech India', 'sales@agritech.in', '9876543212', 'Gujarat, India', 4.9, true],
      ['Bio Solutions', 'support@biosolutions.com', '9876543213', 'Karnataka, India', 4.7, true],
      ['Organic Farms Co', 'hello@organicfarms.co', '9876543214', 'Tamil Nadu, India', 4.5, true]
    ];

    for (const seller of sellersData) {
      await db.query(`
        INSERT INTO sellers (name, email, phone, location, rating, verified)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (email) DO NOTHING
      `, seller);
    }

    // Sample products
    const productsData = [
      [1, 'Premium Rice Seeds (IR64)', 'seeds', 120.00, 'kg', 'High-yield IR64 rice variety suitable for kharif season', '🌾', 1000, true, true, -2.5],
      [2, 'NPK Fertilizer (20:20:0)', 'fertilizer', 850.00, '50kg bag', 'Balanced NPK fertilizer for optimal crop growth', '🌱', 500, true, true, 3.2],
      [3, 'Solar Water Pump', 'equipment', 45000.00, 'unit', '5HP solar-powered water pump with 2-year warranty', '⚡', 50, true, true, -1.8],
      [4, 'Organic Pesticide', 'pesticide', 320.00, 'liter', 'Eco-friendly organic pesticide for crop protection', '🛡️', 0, false, true, 0.5],
      [1, 'Wheat Seeds (HD3086)', 'seeds', 95.00, 'kg', 'Drought-resistant wheat variety for rabi season', '🌾', 800, true, true, 1.2],
      [2, 'Urea Fertilizer', 'fertilizer', 650.00, '50kg bag', 'High-nitrogen urea fertilizer for leafy growth', '🌱', 300, true, true, -0.8],
      [3, 'Drip Irrigation Kit', 'equipment', 12000.00, 'set', 'Complete drip irrigation system for 1 acre', '💧', 75, true, true, 2.5],
      [4, 'Neem Oil', 'pesticide', 180.00, 'liter', 'Natural neem oil for pest and disease control', '🌿', 200, true, true, -1.1]
    ];

    for (const product of productsData) {
      await db.query(`
        INSERT INTO products (seller_id, name, category, price, unit, description, image_url, stock_quantity, in_stock, active, price_change)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
      `, product);
    }

    // Sample market prices
    const marketPricesData = [
      ['Rice', 2100.00, 'quintal', 50.00, 2.4, 'Delhi Mandi', 1200],
      ['Wheat', 2050.00, 'quintal', -30.00, -1.4, 'Punjab Mandi', 950],
      ['Cotton', 5800.00, 'quintal', 120.00, 2.1, 'Gujarat Mandi', 800],
      ['Sugarcane', 320.00, 'quintal', 0.00, 0.0, 'UP Mandi', 1500],
      ['Maize', 1850.00, 'quintal', 25.00, 1.4, 'Karnataka Mandi', 1100],
      ['Soybean', 4200.00, 'quintal', -80.00, -1.9, 'MP Mandi', 700]
    ];

    for (const price of marketPricesData) {
      await db.query(`
        INSERT INTO market_prices (crop_name, current_price, unit, price_change, change_percent, market_name, volume)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
      `, price);
    }

    // Sample market insights
    const insightsData = [
      ['Rice', 'up', 2100.00, 2250.00, 1.15, 'low', ['Punjab', 'Haryana', 'West Bengal'], 'June - July', 35.2],
      ['Cotton', 'up', 5800.00, 6200.00, 1.25, 'medium', ['Gujarat', 'Maharashtra', 'Andhra Pradesh'], 'May - June', 28.7],
      ['Wheat', 'stable', 2050.00, 2100.00, 1.05, 'low', ['Punjab', 'Uttar Pradesh', 'Madhya Pradesh'], 'November - December', 22.1],
      ['Sugarcane', 'down', 320.00, 310.00, 0.95, 'high', ['Uttar Pradesh', 'Maharashtra', 'Karnataka'], 'February - March', 14.0]
    ];

    for (const insight of insightsData) {
      await db.query(`
        INSERT INTO market_insights (crop_name, demand_trend, current_price, projected_price, seasonal_factor, risk_level, best_regions, optimal_timing, market_share)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
      `, insight);
    }

    // Sample weather forecasts
    const weatherData = [
      ['Punjab', 25.0, 35.0, 120.0, 75.0, 'favorable', 'Ideal for rice cultivation'],
      ['Gujarat', 28.0, 38.0, 80.0, 65.0, 'moderate', 'Good for cotton with irrigation'],
      ['Maharashtra', 22.0, 32.0, 150.0, 80.0, 'favorable', 'Excellent for multiple crops'],
      ['Karnataka', 20.0, 30.0, 100.0, 70.0, 'challenging', 'Requires careful water management'],
      ['Tamil Nadu', 24.0, 34.0, 90.0, 78.0, 'moderate', 'Suitable for sugarcane and rice']
    ];

    for (const weather of weatherData) {
      await db.query(`
        INSERT INTO weather_forecasts (region, temperature_min, temperature_max, rainfall, humidity, outlook, agricultural_impact)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
      `, weather);
    }

    // Sample profitability analysis
    const profitabilityData = [
      ['Cotton', 25000.00, 45000.00, 44.4, '6 months', 0.6],
      ['Rice', 18000.00, 28000.00, 35.7, '4 months', 0.3],
      ['Wheat', 15000.00, 22000.00, 31.8, '5 months', 0.2],
      ['Sugarcane', 35000.00, 48000.00, 27.1, '12 months', 0.8],
      ['Maize', 12000.00, 20000.00, 40.0, '3 months', 0.4]
    ];

    for (const profit of profitabilityData) {
      await db.query(`
        INSERT INTO profitability_analysis (crop_name, investment_per_acre, expected_revenue_per_acre, profit_margin, payback_period, risk_factor)
        VALUES ($1, $2, $3, $4, $5, $6)
      `, profit);
    }

    console.log('✅ Sample data seeded successfully!');

  } catch (error) {
    console.error('❌ Error seeding data:', error.message);
    throw error;
  }
};

// Run if called directly
if (require.main === module) {
  seedData()
    .then(() => {
      console.log('🎉 Data seeding completed successfully!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Data seeding failed:', error.message);
      process.exit(1);
    });
}

module.exports = seedData;
