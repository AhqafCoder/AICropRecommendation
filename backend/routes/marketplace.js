const express = require('express');
const router = express.Router();
const db = require('../config/mockDatabase'); // Using mock database
const { validateMarketplaceProduct, validateOrder } = require('../middleware/validation');

// Get all marketplace products
router.get('/products', async (req, res) => {
  try {
    const { category, search, location, minPrice, maxPrice, page = 1, limit = 20 } = req.query;
    
    let query = `
      SELECT p.*, s.name as seller_name, s.location, s.rating as seller_rating,
             AVG(r.rating) as product_rating, COUNT(r.id) as review_count
      FROM products p
      LEFT JOIN sellers s ON p.seller_id = s.id
      LEFT JOIN reviews r ON p.id = r.product_id
      WHERE p.active = true
    `;
    
    const params = [];
    let paramCount = 0;
    
    // Add filters
    if (category && category !== 'all') {
      paramCount++;
      query += ` AND p.category = $${paramCount}`;
      params.push(category);
    }
    
    if (search) {
      paramCount++;
      query += ` AND (p.name ILIKE $${paramCount} OR p.description ILIKE $${paramCount} OR s.name ILIKE $${paramCount})`;
      params.push(`%${search}%`);
    }
    
    if (location) {
      paramCount++;
      query += ` AND s.location ILIKE $${paramCount}`;
      params.push(`%${location}%`);
    }
    
    if (minPrice) {
      paramCount++;
      query += ` AND p.price >= $${paramCount}`;
      params.push(minPrice);
    }
    
    if (maxPrice) {
      paramCount++;
      query += ` AND p.price <= $${paramCount}`;
      params.push(maxPrice);
    }
    
    query += `
      GROUP BY p.id, s.name, s.location, s.rating
      ORDER BY p.created_at DESC
    `;
    
    // Add pagination
    const offset = (page - 1) * limit;
    paramCount++;
    query += ` LIMIT $${paramCount}`;
    params.push(limit);
    
    paramCount++;
    query += ` OFFSET $${paramCount}`;
    params.push(offset);
    
    const result = await db.query(query, params);
    
    // Get total count for pagination
    let countQuery = `
      SELECT COUNT(DISTINCT p.id) as total
      FROM products p
      LEFT JOIN sellers s ON p.seller_id = s.id
      WHERE p.active = true
    `;
    
    const countParams = params.slice(0, -2); // Remove limit and offset
    const countResult = await db.query(countQuery.replace(/ LIMIT.*/, ''), countParams);
    
    res.json({
      products: result.rows.map(row => ({
        id: row.id,
        name: row.name,
        category: row.category,
        price: parseFloat(row.price),
        unit: row.unit,
        seller: row.seller_name,
        location: row.location,
        rating: parseFloat(row.product_rating) || 0,
        reviews: parseInt(row.review_count) || 0,
        inStock: row.in_stock,
        image: row.image_url,
        description: row.description,
        priceChange: parseFloat(row.price_change) || 0
      })),
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total: parseInt(countResult.rows[0].total),
        pages: Math.ceil(countResult.rows[0].total / limit)
      }
    });
  } catch (error) {
    console.error('Error fetching products:', error);
    res.status(500).json({ error: 'Failed to fetch products' });
  }
});

// Get current market prices
router.get('/prices', async (req, res) => {
  try {
    const query = `
      SELECT crop_name, current_price, unit, price_change, 
             change_percent, market_name, last_updated
      FROM market_prices
      WHERE last_updated >= NOW() - INTERVAL '24 hours'
      ORDER BY last_updated DESC
    `;
    
    const result = await db.query(query);
    
    res.json(result.rows.map(row => ({
      crop: row.crop_name,
      currentPrice: parseFloat(row.current_price),
      unit: row.unit,
      change: parseFloat(row.price_change),
      changePercent: parseFloat(row.change_percent),
      market: row.market_name,
      lastUpdated: row.last_updated
    })));
  } catch (error) {
    console.error('Error fetching market prices:', error);
    res.status(500).json({ error: 'Failed to fetch market prices' });
  }
});

// Get market insights
router.get('/insights', async (req, res) => {
  try {
    const query = `
      SELECT crop_name, demand_trend, current_price, projected_price,
             seasonal_factor, risk_level, best_regions, optimal_timing,
             market_share, last_updated
      FROM market_insights
      ORDER BY market_share DESC
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
      marketShare: parseFloat(row.market_share)
    })));
  } catch (error) {
    console.error('Error fetching market insights:', error);
    res.status(500).json({ error: 'Failed to fetch market insights' });
  }
});

// Place an order
router.post('/orders', validateOrder, async (req, res) => {
  try {
    const { productId, quantity, deliveryAddress, contactInfo } = req.body;
    
    // Check product availability
    const productQuery = 'SELECT * FROM products WHERE id = $1 AND active = true AND in_stock = true';
    const productResult = await db.query(productQuery, [productId]);
    
    if (productResult.rows.length === 0) {
      return res.status(404).json({ error: 'Product not found or out of stock' });
    }
    
    const product = productResult.rows[0];
    const totalAmount = product.price * quantity;
    
    // Create order using transaction
    const order = await db.transaction(async (client) => {
      // Insert order
      const orderQuery = `
        INSERT INTO orders (product_id, quantity, total_amount, delivery_address, 
                           contact_info, status, created_at)
        VALUES ($1, $2, $3, $4, $5, 'confirmed', NOW())
        RETURNING *
      `;
      
      const orderResult = await client.query(orderQuery, [
        productId,
        quantity,
        totalAmount,
        JSON.stringify(deliveryAddress),
        JSON.stringify(contactInfo)
      ]);
      
      // Update product stock (if tracking stock)
      if (product.stock_quantity !== null) {
        const updateStockQuery = `
          UPDATE products 
          SET stock_quantity = stock_quantity - $1,
              in_stock = CASE WHEN stock_quantity - $1 <= 0 THEN false ELSE true END
          WHERE id = $2
        `;
        await client.query(updateStockQuery, [quantity, productId]);
      }
      
      return orderResult.rows[0];
    });
    
    res.status(201).json({
      orderId: order.id,
      status: order.status,
      totalAmount: parseFloat(order.total_amount),
      estimatedDelivery: '3-5 days',
      trackingNumber: `TRK${order.id.toString().padStart(6, '0')}`
    });
    
  } catch (error) {
    console.error('Error placing order:', error);
    res.status(500).json({ error: 'Failed to place order' });
  }
});

// Get order history for a user
router.get('/orders/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    
    const query = `
      SELECT o.*, p.name as product_name, p.image_url, s.name as seller_name
      FROM orders o
      JOIN products p ON o.product_id = p.id
      JOIN sellers s ON p.seller_id = s.id
      WHERE o.user_id = $1
      ORDER BY o.created_at DESC
    `;
    
    const result = await db.query(query, [userId]);
    
    res.json(result.rows.map(row => ({
      orderId: row.id,
      productName: row.product_name,
      sellerName: row.seller_name,
      quantity: row.quantity,
      totalAmount: parseFloat(row.total_amount),
      status: row.status,
      orderDate: row.created_at,
      deliveryDate: row.delivered_at,
      trackingNumber: `TRK${row.id.toString().padStart(6, '0')}`
    })));
    
  } catch (error) {
    console.error('Error fetching order history:', error);
    res.status(500).json({ error: 'Failed to fetch order history' });
  }
});

// Add product to favorites
router.post('/favorites', async (req, res) => {
  try {
    const { userId, productId } = req.body;
    
    const query = `
      INSERT INTO favorites (user_id, product_id, created_at)
      VALUES ($1, $2, NOW())
      ON CONFLICT (user_id, product_id) DO NOTHING
      RETURNING *
    `;
    
    const result = await db.query(query, [userId, productId]);
    
    res.json({ success: true, favorite: result.rows[0] });
  } catch (error) {
    console.error('Error adding to favorites:', error);
    res.status(500).json({ error: 'Failed to add to favorites' });
  }
});

module.exports = router;
