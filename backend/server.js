const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests from this IP, please try again later.'
});

// Middleware
app.use(helmet());
app.use(cors({
  origin: ['http://localhost:3000', 'http://localhost:3001'],
  credentials: true
}));
app.use(compression());
app.use(morgan('combined'));
app.use(limiter);
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Import routes
const dashboardRoutes = require('./routes/dashboard');
const marketplaceRoutes = require('./routes/marketplace');

// Use routes
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/marketplace', marketplaceRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '2.0.0',
    service: 'CropAI Backend'
  });
});

// Basic API endpoints
app.get('/', (req, res) => {
  res.json({
    message: 'CropAI Express.js Backend API',
    version: '2.0.0',
    description: 'Comprehensive agricultural marketplace and analytics API',
    status: 'running'
  });
});

// Dashboard stats endpoint
app.get('/api/dashboard/stats', (req, res) => {
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

// Analytics endpoint
app.get('/api/analytics/dashboard', (req, res) => {
  try {
    const analyticsData = {
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
    
    res.json({
      success: true,
      data: analyticsData,
      generatedAt: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      error: 'Failed to fetch analytics data', 
      message: error.message 
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    message: `The route ${req.originalUrl} does not exist on this server.`
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 CropAI Backend Server running on port ${PORT}`);
  console.log(`📊 Analytics API: http://localhost:${PORT}/api/analytics`);
  console.log(`📈 Dashboard API: http://localhost:${PORT}/api/dashboard`);
  console.log(`💚 Health Check: http://localhost:${PORT}/health`);
});

module.exports = app;