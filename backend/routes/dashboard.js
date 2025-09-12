// Dashboard Routes - Express.js
// Handles all dashboard-related API endpoints

const express = require('express');
const router = express.Router();
const { DataGenerator } = require('../models/schemas');

// Get dashboard overview data
router.get('/overview', (req, res) => {
  try {
    const dashboardData = DataGenerator.generateDashboardStats();
    
    res.json({
      success: true,
      data: dashboardData,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch dashboard data', 
      message: error.message 
    });
  }
});

// Get recent activities
router.get('/activities', (req, res) => {
  try {
    const { limit = 10 } = req.query;
    
    const activities = [
      {
        id: 1,
        type: 'sale',
        title: 'Crop Sale Completed',
        description: 'Sold 500kg of wheat at ₹25/kg to ABC Foods',
        amount: 12500,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        status: 'completed',
        icon: 'shopping-cart',
        color: 'green'
      },
      {
        id: 2,
        type: 'alert',
        title: 'Disease Alert',
        description: 'Potential late blight detected in tomato field A-12',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
        status: 'warning',
        icon: 'alert-triangle',
        color: 'orange',
        severity: 'medium'
      },
      {
        id: 3,
        type: 'harvest',
        title: 'Harvest Completed',
        description: 'Successfully harvested 2 tons of rice from field B-05',
        quantity: 2000,
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
        status: 'completed',
        icon: 'package',
        color: 'blue'
      },
      {
        id: 4,
        type: 'maintenance',
        title: 'Equipment Maintenance',
        description: 'Irrigation system maintenance completed in sector C',
        timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
        status: 'completed',
        icon: 'settings',
        color: 'gray'
      },
      {
        id: 5,
        type: 'weather',
        title: 'Weather Update',
        description: 'Rain expected in next 48 hours - prepare drainage',
        timestamp: new Date(Date.now() - 10 * 60 * 60 * 1000).toISOString(),
        status: 'info',
        icon: 'cloud-rain',
        color: 'blue'
      }
    ];

    res.json({
      success: true,
      data: activities.slice(0, parseInt(limit)),
      metadata: {
        total: activities.length,
        limit: parseInt(limit)
      }
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch activities', 
      message: error.message 
    });
  }
});

// Get weather data
router.get('/weather', (req, res) => {
  try {
    const weatherData = {
      current: {
        temperature: 28,
        humidity: 65,
        windSpeed: 12,
        condition: 'Partly Cloudy',
        icon: 'partly-cloudy',
        uvIndex: 6,
        visibility: 10,
        pressure: 1013
      },
      forecast: [
        {
          day: 'Today',
          high: 32,
          low: 24,
          condition: 'Sunny',
          icon: 'sunny',
          precipitation: 0
        },
        {
          day: 'Tomorrow',
          high: 29,
          low: 22,
          condition: 'Rainy',
          icon: 'rainy',
          precipitation: 80
        },
        {
          day: 'Wednesday',
          high: 27,
          low: 20,
          condition: 'Cloudy',
          icon: 'cloudy',
          precipitation: 20
        },
        {
          day: 'Thursday',
          high: 30,
          low: 23,
          condition: 'Partly Cloudy',
          icon: 'partly-cloudy',
          precipitation: 10
        },
        {
          day: 'Friday',
          high: 31,
          low: 25,
          condition: 'Sunny',
          icon: 'sunny',
          precipitation: 0
        }
      ],
      alerts: [
        {
          type: 'rain',
          message: 'Heavy rain expected tomorrow. Prepare drainage systems.',
          severity: 'medium',
          validUntil: new Date(Date.now() + 48 * 60 * 60 * 1000).toISOString()
        }
      ]
    };

    res.json({
      success: true,
      data: weatherData,
      lastUpdated: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch weather data', 
      message: error.message 
    });
  }
});

// Get quick stats for dashboard cards
router.get('/stats', (req, res) => {
  try {
    const stats = [
      {
        title: 'Total Revenue',
        value: '₹12,56,670',
        change: '+18.2%',
        trend: 'up',
        icon: 'dollar-sign',
        color: 'green',
        period: 'This month'
      },
      {
        title: 'Active Crops',
        value: '2,340',
        change: '+12.5%',
        trend: 'up',
        icon: 'leaf',
        color: 'emerald',
        period: 'Current season'
      },
      {
        title: 'Healthy Crops',
        value: '87.5%',
        change: '+5.1%',
        trend: 'up',
        icon: 'shield-check',
        color: 'blue',
        period: 'Real-time'
      },
      {
        title: 'Disease Alerts',
        value: '12',
        change: '-25%',
        trend: 'down',
        icon: 'alert-circle',
        color: 'orange',
        period: 'Last 7 days'
      }
    ];

    res.json({
      success: true,
      data: stats,
      generatedAt: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch dashboard stats', 
      message: error.message 
    });
  }
});

// Get notifications
router.get('/notifications', (req, res) => {
  try {
    const { unreadOnly = false } = req.query;
    
    const notifications = [
      {
        id: 1,
        title: 'New Order Received',
        message: 'ABC Foods placed an order for 1000kg wheat',
        type: 'order',
        read: false,
        priority: 'high',
        timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString()
      },
      {
        id: 2,
        title: 'Disease Alert',
        message: 'Potential disease detected in tomato field A-12',
        type: 'alert',
        read: false,
        priority: 'medium',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
      },
      {
        id: 3,
        title: 'Weather Warning',
        message: 'Heavy rain expected in next 24 hours',
        type: 'weather',
        read: true,
        priority: 'medium',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString()
      }
    ];

    const filteredNotifications = unreadOnly === 'true' 
      ? notifications.filter(n => !n.read)
      : notifications;

    res.json({
      success: true,
      data: filteredNotifications,
      metadata: {
        total: notifications.length,
        unread: notifications.filter(n => !n.read).length
      }
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch notifications', 
      message: error.message 
    });
  }
});

// Mark notification as read
router.patch('/notifications/:id/read', (req, res) => {
  try {
    const { id } = req.params;
    
    // In a real app, update the notification in database
    res.json({
      success: true,
      message: `Notification ${id} marked as read`
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to update notification', 
      message: error.message 
    });
  }
});

module.exports = router;