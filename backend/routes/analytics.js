const express = require('express');
const router = express.Router();
const db = require('../config/mockDatabase'); // Using mock database

// Get market analytics overview
router.get('/overview', async (req, res) => {
  try {
    const { timeframe = '3months' } = req.query;
    
    // Calculate date range based on timeframe
    let dateFilter = '';
    switch (timeframe) {
      case '1month':
        dateFilter = "WHERE created_at >= NOW() - INTERVAL '1 month'";
        break;
      case '3months':
        dateFilter = "WHERE created_at >= NOW() - INTERVAL '3 months'";
        break;
      case '6months':
        dateFilter = "WHERE created_at >= NOW() - INTERVAL '6 months'";
        break;
      case '1year':
        dateFilter = "WHERE created_at >= NOW() - INTERVAL '1 year'";
        break;
      default:
        dateFilter = "WHERE created_at >= NOW() - INTERVAL '3 months'";
    }
    
    // Get key metrics
    const metricsQuery = `
      SELECT 
        COUNT(DISTINCT o.id) as total_orders,
        COALESCE(SUM(o.total_amount), 0) as total_volume,
        COALESCE(AVG(mp.change_percent), 0) as avg_price_growth,
        COUNT(DISTINCT p.id) as active_products
      FROM orders o
      LEFT JOIN market_prices mp ON mp.last_updated >= NOW() - INTERVAL '7 days'
      LEFT JOIN products p ON p.active = true
      ${dateFilter.replace('created_at', 'o.created_at')}
    `;
    
    const metricsResult = await db.query(metricsQuery);
    const metrics = metricsResult.rows[0];
    
    // Get top performing crops
    const topCropsQuery = `
      SELECT crop_name, AVG(change_percent) as avg_growth,
             SUM(CASE WHEN change_percent > 0 THEN 1 ELSE 0 END) as positive_days,
             COUNT(*) as total_days
      FROM market_prices
      WHERE last_updated >= NOW() - INTERVAL '30 days'
      GROUP BY crop_name
      ORDER BY avg_growth DESC
      LIMIT 5
    `;
    
    const topCropsResult = await db.query(topCropsQuery);
    
    res.json({
      metrics: {
        totalOrders: parseInt(metrics.total_orders) || 0,
        totalVolume: parseFloat(metrics.total_volume) || 0,
        avgPriceGrowth: parseFloat(metrics.avg_price_growth) || 0,
        activeProducts: parseInt(metrics.active_products) || 0
      },
      topCrops: topCropsResult.rows.map(row => ({
        crop: row.crop_name,
        avgGrowth: parseFloat(row.avg_growth),
        positiveRatio: parseFloat(row.positive_days) / parseFloat(row.total_days)
      })),
      timeframe
    });
    
  } catch (error) {
    console.error('Error fetching analytics overview:', error);
    res.status(500).json({ error: 'Failed to fetch analytics overview' });
  }
});

// Get crop market analysis
router.get('/crops', async (req, res) => {
  try {
    const query = `
      SELECT 
        mi.crop_name,
        mi.demand_trend,
        mi.current_price,
        mi.projected_price,
        mi.seasonal_factor,
        mi.risk_level,
        mi.best_regions,
        mi.optimal_timing,
        mi.market_share,
        mp.change_percent as recent_change
      FROM market_insights mi
      LEFT JOIN market_prices mp ON mi.crop_name = mp.crop_name 
        AND mp.last_updated >= NOW() - INTERVAL '24 hours'
      ORDER BY mi.market_share DESC
    `;
    
    const result = await db.query(query);
    
    res.json(result.rows.map(row => ({
      crop: row.crop_name,
      demandTrend: row.demand_trend,
      currentPrice: parseFloat(row.current_price),
      projectedPrice: parseFloat(row.projected_price),
      seasonalFactor: parseFloat(row.seasonal_factor),
      riskLevel: row.risk_level,
      bestRegions: row.best_regions,
      optimalPlantingWindow: row.optimal_timing,
      marketShare: parseFloat(row.market_share),
      recentChange: parseFloat(row.recent_change) || 0
    })));
    
  } catch (error) {
    console.error('Error fetching crop analytics:', error);
    res.status(500).json({ error: 'Failed to fetch crop analytics' });
  }
});

// Get weather insights
router.get('/weather', async (req, res) => {
  try {
    const query = `
      SELECT region, temperature_min, temperature_max, rainfall, humidity,
             outlook, agricultural_impact, last_updated
      FROM weather_forecasts
      WHERE last_updated >= NOW() - INTERVAL '24 hours'
      ORDER BY region
    `;
    
    const result = await db.query(query);
    
    res.json(result.rows.map(row => ({
      region: row.region,
      temperature: {
        min: parseFloat(row.temperature_min),
        max: parseFloat(row.temperature_max)
      },
      rainfall: parseFloat(row.rainfall),
      humidity: parseFloat(row.humidity),
      outlook: row.outlook,
      impact: row.agricultural_impact,
      lastUpdated: row.last_updated
    })));
    
  } catch (error) {
    console.error('Error fetching weather insights:', error);
    res.status(500).json({ error: 'Failed to fetch weather insights' });
  }
});

// Get profitability analysis
router.get('/profitability', async (req, res) => {
  try {
    const query = `
      SELECT crop_name, investment_per_acre, expected_revenue_per_acre,
             profit_margin, payback_period, risk_factor, last_updated
      FROM profitability_analysis
      ORDER BY profit_margin DESC
    `;
    
    const result = await db.query(query);
    
    res.json(result.rows.map(row => ({
      crop: row.crop_name,
      investmentPerAcre: parseFloat(row.investment_per_acre),
      expectedRevenuePerAcre: parseFloat(row.expected_revenue_per_acre),
      profitMargin: parseFloat(row.profit_margin),
      paybackPeriod: row.payback_period,
      riskFactor: parseFloat(row.risk_factor),
      lastUpdated: row.last_updated
    })));
    
  } catch (error) {
    console.error('Error fetching profitability analysis:', error);
    res.status(500).json({ error: 'Failed to fetch profitability analysis' });
  }
});

// Get price history for a specific crop
router.get('/prices/:crop/history', async (req, res) => {
  try {
    const { crop } = req.params;
    const { days = 30 } = req.query;
    
    const query = `
      SELECT DATE(last_updated) as date, AVG(current_price) as price,
             SUM(volume) as volume
      FROM market_prices
      WHERE crop_name = $1 AND last_updated >= NOW() - INTERVAL '${days} days'
      GROUP BY DATE(last_updated)
      ORDER BY date ASC
    `;
    
    const result = await db.query(query, [crop]);
    
    res.json(result.rows.map(row => ({
      date: row.date,
      price: parseFloat(row.price),
      volume: parseFloat(row.volume) || 0
    })));
    
  } catch (error) {
    console.error('Error fetching price history:', error);
    res.status(500).json({ error: 'Failed to fetch price history' });
  }
});

// Get regional performance comparison
router.get('/regions', async (req, res) => {
  try {
    const query = `
      SELECT region, crop_name, AVG(yield_per_acre) as avg_yield,
             AVG(profit_per_acre) as avg_profit, COUNT(*) as farmers_count
      FROM farmer_performance fp
      JOIN farmer_profiles fpr ON fp.farmer_id = fpr.id
      WHERE fp.harvest_date >= NOW() - INTERVAL '1 year'
      GROUP BY region, crop_name
      ORDER BY region, avg_profit DESC
    `;
    
    const result = await db.query(query);
    
    // Group by region
    const regionData = {};
    result.rows.forEach(row => {
      if (!regionData[row.region]) {
        regionData[row.region] = [];
      }
      regionData[row.region].push({
        crop: row.crop_name,
        avgYield: parseFloat(row.avg_yield),
        avgProfit: parseFloat(row.avg_profit),
        farmersCount: parseInt(row.farmers_count)
      });
    });
    
    res.json(regionData);
    
  } catch (error) {
    console.error('Error fetching regional analytics:', error);
    res.status(500).json({ error: 'Failed to fetch regional analytics' });
  }
});

module.exports = router;
