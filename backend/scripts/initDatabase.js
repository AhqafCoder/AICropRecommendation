require('dotenv').config();
const { Pool } = require('pg');

// Database initialization script
const initDatabase = async () => {
  const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: 'postgres', // Connect to default database first
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'password'
  });

  try {
    console.log('🔧 Initializing CropAI Database...');

    // Create database if not exists
    await pool.query(`CREATE DATABASE ${process.env.DB_NAME} OWNER ${process.env.DB_USER};`);
    console.log('✅ Database created successfully');

  } catch (error) {
    if (error.code === '42P04') {
      console.log('ℹ️  Database already exists');
    } else {
      console.error('❌ Error creating database:', error.message);
    }
  }

  await pool.end();

  // Connect to the new database
  const appPool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD
  });

  try {
    // Create tables
    console.log('📋 Creating database tables...');

    // Users table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        phone VARCHAR(15),
        location VARCHAR(100),
        farm_size DECIMAL(10,2),
        role VARCHAR(20) DEFAULT 'farmer',
        reset_token VARCHAR(500),
        reset_token_expires TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
      );
    `);

    // Sellers table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS sellers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(15),
        location VARCHAR(100),
        rating DECIMAL(2,1) DEFAULT 0.0,
        verified BOOLEAN DEFAULT false,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Products table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        seller_id INTEGER REFERENCES sellers(id),
        name VARCHAR(200) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        unit VARCHAR(50) NOT NULL,
        description TEXT,
        image_url VARCHAR(500),
        stock_quantity INTEGER,
        in_stock BOOLEAN DEFAULT true,
        active BOOLEAN DEFAULT true,
        price_change DECIMAL(5,2) DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Market prices table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS market_prices (
        id SERIAL PRIMARY KEY,
        crop_name VARCHAR(100) NOT NULL,
        current_price DECIMAL(10,2) NOT NULL,
        unit VARCHAR(20) NOT NULL,
        price_change DECIMAL(10,2) DEFAULT 0.0,
        change_percent DECIMAL(5,2) DEFAULT 0.0,
        market_name VARCHAR(100),
        volume INTEGER DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Market insights table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS market_insights (
        id SERIAL PRIMARY KEY,
        crop_name VARCHAR(100) NOT NULL,
        demand_trend VARCHAR(20) NOT NULL,
        current_price DECIMAL(10,2) NOT NULL,
        projected_price DECIMAL(10,2) NOT NULL,
        seasonal_factor DECIMAL(3,2) DEFAULT 1.0,
        risk_level VARCHAR(20) NOT NULL,
        best_regions TEXT[],
        optimal_timing VARCHAR(100),
        market_share DECIMAL(5,2) DEFAULT 0.0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Orders table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        delivery_address JSONB NOT NULL,
        contact_info JSONB NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        delivered_at TIMESTAMP
      );
    `);

    // Crop predictions table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS crop_predictions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        nitrogen DECIMAL(5,2) NOT NULL,
        phosphorus DECIMAL(5,2) NOT NULL,
        potassium DECIMAL(5,2) NOT NULL,
        temperature DECIMAL(4,1) NOT NULL,
        humidity DECIMAL(4,1) NOT NULL,
        ph DECIMAL(3,1) NOT NULL,
        rainfall DECIMAL(6,1) NOT NULL,
        area_ha DECIMAL(6,2),
        previous_crop VARCHAR(100),
        season VARCHAR(20),
        region VARCHAR(100),
        recommended_crop VARCHAR(100),
        confidence DECIMAL(4,3),
        prediction_data JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Disease detections table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS disease_detections (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        crop_type VARCHAR(100),
        detected_disease VARCHAR(100),
        confidence DECIMAL(4,3),
        severity VARCHAR(20),
        treatment_recommendation TEXT,
        image_url VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Reviews table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        product_id INTEGER REFERENCES products(id),
        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
        comment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Favorites table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS favorites (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        product_id INTEGER REFERENCES products(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id)
      );
    `);

    // Weather forecasts table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS weather_forecasts (
        id SERIAL PRIMARY KEY,
        region VARCHAR(100) NOT NULL,
        temperature_min DECIMAL(4,1),
        temperature_max DECIMAL(4,1),
        rainfall DECIMAL(6,1),
        humidity DECIMAL(4,1),
        outlook VARCHAR(50),
        agricultural_impact TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Profitability analysis table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS profitability_analysis (
        id SERIAL PRIMARY KEY,
        crop_name VARCHAR(100) NOT NULL,
        investment_per_acre DECIMAL(10,2),
        expected_revenue_per_acre DECIMAL(10,2),
        profit_margin DECIMAL(5,2),
        payback_period VARCHAR(50),
        risk_factor DECIMAL(3,2),
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Farmer profiles table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS farmer_profiles (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        region VARCHAR(100),
        primary_crops TEXT[],
        farming_experience INTEGER,
        farm_type VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Farmer performance table
    await appPool.query(`
      CREATE TABLE IF NOT EXISTS farmer_performance (
        id SERIAL PRIMARY KEY,
        farmer_id INTEGER REFERENCES users(id),
        crop_name VARCHAR(100),
        yield_per_acre DECIMAL(6,2),
        profit_per_acre DECIMAL(10,2),
        harvest_date DATE,
        season VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Create indexes for better performance
    console.log('🚀 Creating database indexes...');

    await appPool.query('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);');
    await appPool.query('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);');
    await appPool.query('CREATE INDEX IF NOT EXISTS idx_products_seller ON products(seller_id);');
    await appPool.query('CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);');
    await appPool.query('CREATE INDEX IF NOT EXISTS idx_predictions_user ON crop_predictions(user_id);');
    await appPool.query('CREATE INDEX IF NOT EXISTS idx_market_prices_crop ON market_prices(crop_name);');
    await appPool.query('CREATE INDEX IF NOT EXISTS idx_market_prices_updated ON market_prices(last_updated);');

    console.log('✅ Database tables created successfully!');
    console.log('📊 Database initialization completed!');

  } catch (error) {
    console.error('❌ Error creating tables:', error.message);
    throw error;
  } finally {
    await appPool.end();
  }
};

// Run if called directly
if (require.main === module) {
  initDatabase()
    .then(() => {
      console.log('🎉 Database initialization completed successfully!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Database initialization failed:', error.message);
      process.exit(1);
    });
}

module.exports = initDatabase;
