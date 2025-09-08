const express = require('express');
const router = express.Router();
const db = require('../config/mockDatabase'); // Using mock database

// Get user profile
router.get('/profile', async (req, res) => {
  try {
    const userId = req.user.userId;
    
    const query = `
      SELECT id, name, email, phone, location, farm_size, created_at, last_login
      FROM users WHERE id = $1
    `;
    
    const result = await db.query(query, [userId]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    const user = result.rows[0];
    res.json({
      id: user.id,
      name: user.name,
      email: user.email,
      phone: user.phone,
      location: user.location,
      farmSize: user.farm_size,
      createdAt: user.created_at,
      lastLogin: user.last_login
    });
    
  } catch (error) {
    console.error('Error fetching user profile:', error);
    res.status(500).json({ error: 'Failed to fetch user profile' });
  }
});

// Update user profile
router.put('/profile', async (req, res) => {
  try {
    const userId = req.user.userId;
    const { name, phone, location, farmSize } = req.body;
    
    const query = `
      UPDATE users 
      SET name = $1, phone = $2, location = $3, farm_size = $4, updated_at = NOW()
      WHERE id = $5
      RETURNING id, name, email, phone, location, farm_size, updated_at
    `;
    
    const result = await db.query(query, [name, phone, location, farmSize, userId]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({
      success: true,
      user: result.rows[0]
    });
    
  } catch (error) {
    console.error('Error updating user profile:', error);
    res.status(500).json({ error: 'Failed to update user profile' });
  }
});

// Get user dashboard stats
router.get('/dashboard', async (req, res) => {
  try {
    const userId = req.user.userId;
    
    // Get user's predictions count
    const predictionsQuery = 'SELECT COUNT(*) as count FROM crop_predictions WHERE user_id = $1';
    const predictionsResult = await db.query(predictionsQuery, [userId]);
    
    // Get user's orders count
    const ordersQuery = 'SELECT COUNT(*) as count FROM orders WHERE user_id = $1';
    const ordersResult = await db.query(ordersQuery, [userId]);
    
    // Get user's favorites count
    const favoritesQuery = 'SELECT COUNT(*) as count FROM favorites WHERE user_id = $1';
    const favoritesResult = await db.query(favoritesQuery, [userId]);
    
    // Get recent activity
    const activityQuery = `
      SELECT 'prediction' as type, created_at, recommended_crop as details
      FROM crop_predictions WHERE user_id = $1
      UNION ALL
      SELECT 'order' as type, created_at, total_amount::text as details
      FROM orders WHERE user_id = $1
      ORDER BY created_at DESC
      LIMIT 10
    `;
    const activityResult = await db.query(activityQuery, [userId]);
    
    res.json({
      stats: {
        predictions: parseInt(predictionsResult.rows[0].count),
        orders: parseInt(ordersResult.rows[0].count),
        favorites: parseInt(favoritesResult.rows[0].count)
      },
      recentActivity: activityResult.rows
    });
    
  } catch (error) {
    console.error('Error fetching user dashboard:', error);
    res.status(500).json({ error: 'Failed to fetch dashboard data' });
  }
});

module.exports = router;
