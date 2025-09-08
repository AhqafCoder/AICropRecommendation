const Joi = require('joi');

// Validation schemas
const cropPredictionSchema = Joi.object({
  N: Joi.number().min(0).max(200).required(),
  P: Joi.number().min(0).max(150).required(),
  K: Joi.number().min(0).max(200).required(),
  temperature: Joi.number().min(-10).max(55).required(),
  humidity: Joi.number().min(0).max(100).required(),
  ph: Joi.number().min(3.5).max(9.0).required(),
  rainfall: Joi.number().min(0).max(5000).required(),
  area_ha: Joi.number().min(0.1).max(1000).optional(),
  previous_crop: Joi.string().allow('').optional(),
  season: Joi.string().valid('kharif', 'rabi', 'zaid').optional(),
  region: Joi.string().optional()
});

const orderSchema = Joi.object({
  productId: Joi.string().required(),
  quantity: Joi.number().positive().required(),
  deliveryAddress: Joi.object({
    street: Joi.string().required(),
    city: Joi.string().required(),
    state: Joi.string().required(),
    pincode: Joi.string().pattern(/^\d{6}$/).required()
  }).required(),
  contactInfo: Joi.object({
    name: Joi.string().required(),
    phone: Joi.string().pattern(/^\d{10}$/).required(),
    email: Joi.string().email().required()
  }).required()
});

const registrationSchema = Joi.object({
  name: Joi.string().min(2).max(100).required(),
  email: Joi.string().email().required(),
  password: Joi.string().min(8).pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/).required(),
  phone: Joi.string().pattern(/^\d{10}$/).required(),
  location: Joi.string().required(),
  farmSize: Joi.number().positive().optional()
});

const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required()
});

const marketplaceProductSchema = Joi.object({
  name: Joi.string().min(2).max(200).required(),
  category: Joi.string().valid('seeds', 'fertilizer', 'equipment', 'pesticide').required(),
  price: Joi.number().positive().required(),
  unit: Joi.string().required(),
  description: Joi.string().max(1000).required(),
  imageUrl: Joi.string().uri().optional(),
  stockQuantity: Joi.number().min(0).optional()
});

// Validation middleware factory
const validate = (schema) => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, { 
      abortEarly: false,
      stripUnknown: true 
    });
    
    if (error) {
      const errorMessages = error.details.map(detail => detail.message);
      return res.status(400).json({ 
        error: 'Validation failed',
        details: errorMessages 
      });
    }
    
    req.body = value;
    next();
  };
};

// Specific validation middleware
const validateCropPrediction = validate(cropPredictionSchema);
const validateOrder = validate(orderSchema);
const validateRegistration = validate(registrationSchema);
const validateLogin = validate(loginSchema);
const validateMarketplaceProduct = validate(marketplaceProductSchema);

// Query parameter validation
const validatePagination = (req, res, next) => {
  const { page = 1, limit = 20 } = req.query;
  
  const pageNum = parseInt(page);
  const limitNum = parseInt(limit);
  
  if (isNaN(pageNum) || pageNum < 1) {
    return res.status(400).json({ error: 'Invalid page number' });
  }
  
  if (isNaN(limitNum) || limitNum < 1 || limitNum > 100) {
    return res.status(400).json({ error: 'Invalid limit (must be 1-100)' });
  }
  
  req.pagination = { page: pageNum, limit: limitNum };
  next();
};

module.exports = {
  validateCropPrediction,
  validateOrder,
  validateRegistration,
  validateLogin,
  validateMarketplaceProduct,
  validatePagination
};
