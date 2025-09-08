require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');

// Import routes
const authRoutes = require('./routes/auth');
const cropRoutes = require('./routes/crops');
const marketplaceRoutes = require('./routes/marketplace');
const analyticsRoutes = require('./routes/analytics');
const userRoutes = require('./routes/users');

// Import middleware
const { errorHandler } = require('./middleware/errorHandler');
const { authenticateToken } = require('./middleware/auth');

// Import database
const db = require('./config/mockDatabase'); // Using mock database for now

const app = express();
const PORT = process.env.PORT || 5000;

// Security middleware
app.use(helmet());
app.use(compression());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// CORS configuration
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3001',
  credentials: true,
  optionsSuccessStatus: 200
}));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging middleware
app.use(morgan('combined'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: '1.0.0'
  });
});

// API routes
app.use('/api/auth', authRoutes);
app.use('/api/crops', cropRoutes);
app.use('/api/marketplace', marketplaceRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/users', authenticateToken, userRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'CropAI Backend API',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      auth: '/api/auth',
      crops: '/api/crops',
      marketplace: '/api/marketplace',
      analytics: '/api/analytics',
      users: '/api/users'
    },
    documentation: '/api/docs'
  });
});

// Error handling middleware (must be last)
app.use(errorHandler);

// Start server
const startServer = async () => {
  try {
    // Test database connection
    await db.testConnection();
    console.log('✅ Database connected successfully');
    
    app.listen(PORT, () => {
      console.log(`🚀 CropAI Backend Server running on port ${PORT}`);
      console.log(`🌐 Health check: http://localhost:${PORT}/health`);
      console.log(`📚 API docs: http://localhost:${PORT}/api/docs`);
      console.log(`🔧 Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error.message);
    process.exit(1);
  }
};

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});

startServer();

module.exports = app;
