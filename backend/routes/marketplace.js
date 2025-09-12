const express = require('express');
const router = express.Router();

const { productSchema, DataGenerator } = require('../models/schemas');

// In-memory storage for products (replace with database in production)
let products = DataGenerator.generateProducts(50);

// Get all products with filtering and pagination
router.get('/products', (req, res) => {
  try {
    const { 
      category, 
      location, 
      minPrice, 
      maxPrice, 
      inStock, 
      search, 
      page = 1, 
      limit = 20,
      sortBy = 'dateAdded',
      sortOrder = 'desc'
    } = req.query;

    let filteredProducts = [...products];

    // Apply filters
    if (category) {
      filteredProducts = filteredProducts.filter(p => p.category === category);
    }

    if (location) {
      filteredProducts = filteredProducts.filter(p => 
        p.location.toLowerCase().includes(location.toLowerCase())
      );
    }

    if (minPrice) {
      filteredProducts = filteredProducts.filter(p => p.price >= parseFloat(minPrice));
    }

    if (maxPrice) {
      filteredProducts = filteredProducts.filter(p => p.price <= parseFloat(maxPrice));
    }

    if (inStock === 'true') {
      filteredProducts = filteredProducts.filter(p => p.inStock);
    }

    if (search) {
      const searchTerm = search.toLowerCase();
      filteredProducts = filteredProducts.filter(p => 
        p.name.toLowerCase().includes(searchTerm) ||
        p.description.toLowerCase().includes(searchTerm) ||
        p.seller.toLowerCase().includes(searchTerm)
      );
    }

    // Apply sorting
    filteredProducts.sort((a, b) => {
      let aVal = a[sortBy];
      let bVal = b[sortBy];
      
      if (sortBy === 'price' || sortBy === 'rating') {
        aVal = parseFloat(aVal);
        bVal = parseFloat(bVal);
      }
      
      if (sortOrder === 'desc') {
        return bVal > aVal ? 1 : -1;
      } else {
        return aVal > bVal ? 1 : -1;
      }
    });

    // Apply pagination
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + parseInt(limit);
    const paginatedProducts = filteredProducts.slice(startIndex, endIndex);

    res.json({
      products: paginatedProducts,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(filteredProducts.length / limit),
        totalProducts: filteredProducts.length,
        hasNext: endIndex < filteredProducts.length,
        hasPrev: startIndex > 0
      },
      filters: {
        category,
        location,
        minPrice,
        maxPrice,
        inStock,
        search
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch products', message: error.message });
  }
});

// Get single product by ID
router.get('/products/:id', (req, res) => {
  try {
    const product = products.find(p => p.id === req.params.id);
    
    if (!product) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    res.json(product);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch product', message: error.message });
  }
});

// Create new product
router.post('/products', (req, res) => {
  try {
    const { error, value } = productSchema.validate(req.body);
    
    if (error) {
      return res.status(400).json({ 
        error: 'Validation failed', 
        details: error.details.map(d => d.message)
      });
    }
    
    const newProduct = {
      ...value,
      id: `prod_${Date.now()}`,
      dateAdded: new Date().toISOString()
    };
    
    products.push(newProduct);
    res.status(201).json(newProduct);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create product', message: error.message });
  }
});

// Update product
router.put('/products/:id', (req, res) => {
  try {
    const productIndex = products.findIndex(p => p.id === req.params.id);
    
    if (productIndex === -1) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    const { error, value } = productSchema.validate(req.body);
    
    if (error) {
      return res.status(400).json({ 
        error: 'Validation failed', 
        details: error.details.map(d => d.message)
      });
    }
    
    products[productIndex] = { ...products[productIndex], ...value };
    res.json(products[productIndex]);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update product', message: error.message });
  }
});

// Delete product
router.delete('/products/:id', (req, res) => {
  try {
    const productIndex = products.findIndex(p => p.id === req.params.id);
    
    if (productIndex === -1) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    const deletedProduct = products.splice(productIndex, 1)[0];
    res.json({ message: 'Product deleted successfully', product: deletedProduct });
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete product', message: error.message });
  }
});

// Get product categories
router.get('/categories', (req, res) => {
  try {
    const categories = [...new Set(products.map(p => p.category))];
    const categoryStats = categories.map(category => ({
      name: category,
      count: products.filter(p => p.category === category).length,
      averagePrice: products
        .filter(p => p.category === category)
        .reduce((sum, p) => sum + p.price, 0) / 
        products.filter(p => p.category === category).length
    }));
    
    res.json(categoryStats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch categories', message: error.message });
  }
});

// Get marketplace statistics
router.get('/stats', (req, res) => {
  try {
    const stats = {
      totalProducts: products.length,
      totalSellers: [...new Set(products.map(p => p.sellerId))].length,
      averagePrice: products.reduce((sum, p) => sum + p.price, 0) / products.length,
      categoriesCount: [...new Set(products.map(p => p.category))].length,
      inStockProducts: products.filter(p => p.inStock).length,
      outOfStockProducts: products.filter(p => !p.inStock).length,
      topRatedProducts: products
        .filter(p => p.rating >= 4.5)
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 5),
      recentProducts: products
        .sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
        .slice(0, 10)
    };
    
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch marketplace stats', message: error.message });
  }
});

// Search suggestions
router.get('/search/suggestions', (req, res) => {
  try {
    const { q } = req.query;
    
    if (!q || q.length < 2) {
      return res.json([]);
    }
    
    const searchTerm = q.toLowerCase();
    const suggestions = [
      ...new Set([
        ...products
          .filter(p => p.name.toLowerCase().includes(searchTerm))
          .map(p => p.name)
          .slice(0, 5),
        ...products
          .filter(p => p.category.toLowerCase().includes(searchTerm))
          .map(p => p.category)
          .slice(0, 3)
      ])
    ].slice(0, 8);
    
    res.json(suggestions);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch suggestions', message: error.message });
  }
});

module.exports = router;
