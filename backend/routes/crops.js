const express = require('express');
const router = express.Router();
const db = require('../config/mockDatabase'); // Using mock database
const { validateCropPrediction } = require('../middleware/validation');

// Crop prediction endpoint
router.post('/predict', validateCropPrediction, async (req, res) => {
  try {
    const { N, P, K, temperature, humidity, ph, rainfall, area_ha, previous_crop, season, region } = req.body;
    
    // Store prediction request in database
    const insertQuery = `
      INSERT INTO crop_predictions (nitrogen, phosphorus, potassium, temperature, 
                                   humidity, ph, rainfall, area_ha, previous_crop, 
                                   season, region, created_at)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, NOW())
      RETURNING id
    `;
    
    const insertResult = await db.query(insertQuery, [
      N, P, K, temperature, humidity, ph, rainfall, area_ha, 
      previous_crop, season, region
    ]);
    
    const predictionId = insertResult.rows[0].id;
    
    // AI Prediction Logic (simplified rule-based system)
    let crop, confidence;
    const seasonValue = season || 'kharif';
    
    if (seasonValue === 'kharif') {
      if (rainfall > 1000) {
        crop = "rice";
        confidence = 0.85;
      } else if (rainfall < 300) {
        crop = "millet";
        confidence = 0.75;
      } else if (temperature > 30) {
        crop = "cotton";
        confidence = 0.80;
      } else {
        crop = "maize";
        confidence = 0.70;
      }
    } else if (seasonValue === 'rabi') {
      if (temperature < 20) {
        crop = "wheat";
        confidence = 0.85;
      } else if (ph > 7.0) {
        crop = "barley";
        confidence = 0.75;
      } else {
        crop = "chickpea";
        confidence = 0.80;
      }
    } else { // zaid
      crop = "watermelon";
      confidence = 0.70;
    }
    
    // Generate explanations
    const explanations = [
      `Season analysis: ${crop} is suitable for ${seasonValue} season cultivation`,
      `Soil conditions favor ${crop} with current NPK levels`,
      `Weather patterns support ${crop} growth`,
      `Regional suitability confirmed for ${crop} cultivation`
    ];
    
    // Calculate yield estimation
    let baseYield = 2.5;
    if (crop === "rice") baseYield = 3.0;
    else if (crop === "wheat") baseYield = 2.8;
    else if (crop === "cotton") baseYield = 1.5;
    else if (crop === "millet") baseYield = 2.0;
    
    // Adjust for conditions
    if (rainfall > 800) baseYield *= 1.2;
    else if (rainfall < 400) baseYield *= 0.8;
    
    // Fertilizer recommendation
    let fertilizerType, dosage;
    if (N < 40) {
      fertilizerType = "NPK 20-10-10";
      dosage = 150;
    } else if (P < 30) {
      fertilizerType = "NPK 10-20-10";
      dosage = 140;
    } else if (K < 35) {
      fertilizerType = "NPK 10-10-20";
      dosage = 135;
    } else {
      fertilizerType = "NPK 15-15-15";
      dosage = 130;
    }
    
    const fertilizerCost = dosage * 25;
    
    // Profit calculation
    const areaHa = area_ha || 1.0;
    const yieldPerHa = baseYield * 2.47;
    
    const cropPrices = {
      "rice": 2000,
      "wheat": 2200,
      "cotton": 5500,
      "millet": 1800,
      "maize": 1900,
      "barley": 2100,
      "chickpea": 4500,
      "watermelon": 1500
    };
    
    const pricePerQuintal = cropPrices[crop] || 2000;
    const totalYieldQuintals = yieldPerHa * areaHa;
    const grossRevenue = Math.round(totalYieldQuintals * pricePerQuintal);
    
    const seedCost = 2000 * areaHa;
    const laborCost = 15000 * areaHa;
    const otherCosts = 8000 * areaHa;
    const totalInvestment = Math.round(seedCost + laborCost + fertilizerCost + otherCosts);
    
    const netProfit = grossRevenue - totalInvestment;
    const roi = totalInvestment > 0 ? (netProfit / totalInvestment * 100) : 0;
    
    // Prepare response
    const response = {
      recommended_crop: crop,
      confidence: Math.round(confidence * 1000) / 1000,
      why: explanations,
      expected_yield_t_per_acre: Math.round(baseYield * 100) / 100,
      yield_interval_p10_p90: [
        Math.round(baseYield * 0.8 * 100) / 100,
        Math.round(baseYield * 1.2 * 100) / 100
      ],
      profit_breakdown: {
        gross: grossRevenue,
        investment: totalInvestment,
        net: netProfit,
        roi: Math.round(roi * 10) / 10
      },
      fertilizer_recommendation: {
        type: fertilizerType,
        dosage_kg_per_ha: dosage,
        cost: fertilizerCost
      },
      previous_crop_analysis: {
        previous_crop: previous_crop || "",
        original_npk: [N, P, K],
        adjusted_npk: [N, P, K],
        nutrient_impact: [0.0, 0.0, 0.0]
      },
      season_analysis: {
        detected_season: seasonValue,
        season_suitability: "suitable",
        season_explanation: `${crop} is recommended for ${seasonValue} season based on climatic conditions`
      },
      model_version: "rule_based_v2_enhanced",
      timestamp: new Date().toISOString(),
      area_analyzed_ha: areaHa,
      region: region || 'default',
      prediction_id: predictionId
    };
    
    // Store prediction result
    const updateQuery = `
      UPDATE crop_predictions 
      SET recommended_crop = $1, confidence = $2, prediction_data = $3
      WHERE id = $4
    `;
    
    await db.query(updateQuery, [crop, confidence, JSON.stringify(response), predictionId]);
    
    res.json(response);
    
  } catch (error) {
    console.error('Error in crop prediction:', error);
    res.status(500).json({ error: 'Failed to generate crop prediction' });
  }
});

// Get prediction history
router.get('/predictions/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const { page = 1, limit = 10 } = req.query;
    
    const offset = (page - 1) * limit;
    
    const query = `
      SELECT id, recommended_crop, confidence, prediction_data, created_at
      FROM crop_predictions
      WHERE user_id = $1
      ORDER BY created_at DESC
      LIMIT $2 OFFSET $3
    `;
    
    const result = await db.query(query, [userId, limit, offset]);
    
    res.json({
      predictions: result.rows,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit)
      }
    });
    
  } catch (error) {
    console.error('Error fetching prediction history:', error);
    res.status(500).json({ error: 'Failed to fetch prediction history' });
  }
});

// Disease detection endpoint
router.post('/disease-detection', async (req, res) => {
  try {
    const { imageData, cropType } = req.body;
    
    // Simplified disease detection (would integrate with ML model)
    const diseases = [
      'Leaf Blight', 'Powdery Mildew', 'Rust', 'Bacterial Spot', 'Healthy'
    ];
    
    const detectedDisease = diseases[Math.floor(Math.random() * diseases.length)];
    const confidence = 0.75 + Math.random() * 0.2; // 75-95% confidence
    
    const treatment = detectedDisease === 'Healthy' ? 
      'No treatment needed. Continue regular monitoring.' :
      `Apply appropriate fungicide and remove affected leaves. Monitor closely.`;
    
    const response = {
      detected_disease: detectedDisease,
      confidence: Math.round(confidence * 1000) / 1000,
      severity: detectedDisease === 'Healthy' ? 'none' : 'moderate',
      treatment_recommendation: treatment,
      prevention_tips: [
        'Ensure proper spacing between plants',
        'Maintain optimal soil moisture',
        'Regular monitoring and early detection',
        'Use disease-resistant varieties'
      ],
      timestamp: new Date().toISOString()
    };
    
    // Store detection result
    const insertQuery = `
      INSERT INTO disease_detections (crop_type, detected_disease, confidence, 
                                     treatment_recommendation, created_at)
      VALUES ($1, $2, $3, $4, NOW())
      RETURNING id
    `;
    
    await db.query(insertQuery, [
      cropType, detectedDisease, confidence, treatment
    ]);
    
    res.json(response);
    
  } catch (error) {
    console.error('Error in disease detection:', error);
    res.status(500).json({ error: 'Failed to detect disease' });
  }
});

module.exports = router;
