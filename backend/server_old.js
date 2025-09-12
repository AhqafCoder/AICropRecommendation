/**
 * CropAI Express.js Backend Server
 * Comprehensive agricultural marketplace and analytics API
 * Version 2.0.0
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const { v4: uuidv4 } = require('uuid');
require('dotenv').config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 8001;

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
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

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '2.0.0',
    service: 'CropAI Backend'
  });
});

// API Documentation endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'CropAI Express.js Backend API',
    version: '2.0.0',
    description: 'Comprehensive agricultural marketplace and analytics API',
    endpoints: {
      health: 'GET /health',
      analytics: 'GET /api/analytics/*',
      marketplace: 'GET /api/marketplace/*',
      dashboard: 'GET /api/dashboard/*',
      docs: 'This endpoint'
    },
    documentation: '/docs'
  });
});

// Import route modules
const analyticsRoutes = require('./routes/analytics');
const marketplaceRoutes = require('./routes/marketplace');
const dashboardRoutes = require('./routes/dashboard');

// API Routes
app.use('/api/analytics', analyticsRoutes);
app.use('/api/marketplace', marketplaceRoutes);
app.use('/api/dashboard', dashboardRoutes);

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
  console.log(`🛒 Marketplace API: http://localhost:${PORT}/api/marketplace`);
  console.log(`📈 Dashboard API: http://localhost:${PORT}/api/dashboard`);
  console.log(`💚 Health Check: http://localhost:${PORT}/health`);
});

module.exports = app;