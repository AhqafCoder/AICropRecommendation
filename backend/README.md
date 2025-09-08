# CropAI Backend - Express.js + PostgreSQL

A robust, scalable backend API for the CropAI agricultural platform built with Express.js and PostgreSQL.

## 🚀 Features

- **RESTful API** with Express.js
- **PostgreSQL Database** for data persistence
- **JWT Authentication** for secure user management
- **Comprehensive Validation** with Joi
- **Error Handling** middleware
- **Rate Limiting** for API protection
- **CORS** enabled for frontend integration
- **Database Migrations** and seeding
- **Production-ready** architecture

## 📋 Prerequisites

Before running the backend, ensure you have:

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **PostgreSQL** (v12 or higher)

## 🛠️ Installation

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Database Setup

#### Install PostgreSQL
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql`
- **Linux**: `sudo apt-get install postgresql postgresql-contrib`

#### Create Database User
```sql
-- Connect to PostgreSQL as admin
psql -U postgres

-- Create user and database
CREATE USER cropai_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE cropai_db OWNER cropai_user;
GRANT ALL PRIVILEGES ON DATABASE cropai_db TO cropai_user;
\q
```

### 3. Environment Configuration

Copy the `.env` file and update the values:

```bash
cp .env.example .env
```

Update `.env` with your configuration:
```env
NODE_ENV=development
PORT=5000

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cropai_db
DB_USER=cropai_user
DB_PASSWORD=your_secure_password

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_EXPIRES_IN=7d

# Frontend URL
FRONTEND_URL=http://localhost:3001
```

### 4. Initialize Database

```bash
# Initialize database tables
npm run init-db

# Seed sample data (optional)
npm run seed
```

### 5. Start the Server

```bash
# Development mode with auto-reload
npm run dev

# Production mode
npm start
```

The server will start on `http://localhost:5000`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### Crop Prediction
- `POST /api/crops/predict` - Get crop recommendation
- `GET /api/crops/predictions/:userId` - Get prediction history
- `POST /api/crops/disease-detection` - Detect crop diseases

### Marketplace
- `GET /api/marketplace/products` - Get marketplace products
- `GET /api/marketplace/prices` - Get current market prices
- `GET /api/marketplace/insights` - Get market insights
- `POST /api/marketplace/orders` - Place an order
- `GET /api/marketplace/orders/:userId` - Get order history
- `POST /api/marketplace/favorites` - Add to favorites

### Analytics
- `GET /api/analytics/overview` - Get market analytics overview
- `GET /api/analytics/crops` - Get crop market analysis
- `GET /api/analytics/weather` - Get weather insights
- `GET /api/analytics/profitability` - Get profitability analysis
- `GET /api/analytics/prices/:crop/history` - Get price history
- `GET /api/analytics/regions` - Get regional performance

### User Management
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `GET /api/users/dashboard` - Get user dashboard stats

## 🗄️ Database Schema

### Core Tables
- **users** - User accounts and profiles
- **sellers** - Marketplace sellers
- **products** - Marketplace products
- **orders** - Purchase orders
- **market_prices** - Real-time crop prices
- **market_insights** - Market analysis data
- **crop_predictions** - AI prediction history
- **disease_detections** - Disease detection results
- **weather_forecasts** - Weather data
- **profitability_analysis** - Crop profitability data

## 🔒 Security Features

- **JWT Authentication** with secure tokens
- **Password Hashing** with bcrypt
- **Request Validation** with Joi schemas
- **Rate Limiting** to prevent abuse
- **CORS** configuration
- **Helmet** for security headers
- **Environment Variable** protection

## 📊 Sample Data

The backend includes sample data for testing:
- 5 verified sellers
- 8 products across categories
- Market prices for 6 major crops
- Weather forecasts for 5 regions
- Profitability analysis for 5 crops

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

## 🚀 Deployment

### Environment Variables for Production
```env
NODE_ENV=production
PORT=5000
DB_HOST=your-production-db-host
JWT_SECRET=your-production-jwt-secret
# ... other production configs
```

### Docker Deployment (Optional)
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5000
CMD ["npm", "start"]
```

## 📈 Performance Optimizations

- **Database Indexing** on frequently queried columns
- **Connection Pooling** for database connections
- **Request Compression** with gzip
- **Caching Headers** for static responses
- **Query Optimization** for complex analytics

## 🛠️ Development Tools

- **Nodemon** for auto-restart during development
- **ESLint** for code linting
- **Jest** for testing
- **Morgan** for request logging
- **Joi** for input validation

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL service
sudo service postgresql status

# Restart PostgreSQL
sudo service postgresql restart

# Check connection
psql -U cropai_user -d cropai_db -h localhost
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 PID
```

### Environment Variables Not Loading
- Ensure `.env` file is in the backend root directory
- Check for typos in variable names
- Restart the server after changes

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support, please contact the development team or create an issue in the repository.
