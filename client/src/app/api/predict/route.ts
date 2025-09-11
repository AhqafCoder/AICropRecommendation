import { NextRequest, NextResponse } from 'next/server';

interface PredictionRequest {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
  area_ha: number;
  region: string;
  previous_crop: string;
  season: string;
  planting_date: string;
}

interface PredictionResponse {
  recommended_crop: string;
  confidence: number;
  expected_yield_t_per_acre: number;
  profit_breakdown: {
    gross: number;
    investment: number;
    net: number;
    roi: number;
  };
  yield_interval_p10_p90: [number, number];
  previous_crop_analysis?: {
    previous_crop: string;
    original_npk: [number, number, number];
    adjusted_npk: [number, number, number];
    nutrient_impact: string;
  };
  season_analysis?: {
    detected_season: string;
    season_suitability: string;
    season_explanation: string;
  };
  fertilizer_recommendation?: {
    type: string;
    dosage_kg_per_ha: number;
    cost: number;
  };
  why?: string[];
  model_version: string;
  timestamp: string;
  error?: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: PredictionRequest = await request.json();

    // Validate required fields
    const requiredFields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'area_ha'];
    for (const field of requiredFields) {
      if (body[field as keyof PredictionRequest] === undefined || body[field as keyof PredictionRequest] === null) {
        return NextResponse.json(
          { error: `Missing required field: ${field}` },
          { status: 400 }
        );
      }
    }

    // Validate numeric ranges
    const validations = [
      { field: 'N', min: 0, max: 300, value: body.N },
      { field: 'P', min: 0, max: 200, value: body.P },
      { field: 'K', min: 0, max: 300, value: body.K },
      { field: 'temperature', min: -10, max: 60, value: body.temperature },
      { field: 'humidity', min: 0, max: 100, value: body.humidity },
      { field: 'ph', min: 0, max: 14, value: body.ph },
      { field: 'rainfall', min: 0, max: 10000, value: body.rainfall },
      { field: 'area_ha', min: 0.01, max: 10000, value: body.area_ha },
    ];

    for (const validation of validations) {
      if (validation.value < validation.min || validation.value > validation.max) {
        return NextResponse.json(
          { error: `${validation.field} must be between ${validation.min} and ${validation.max}` },
          { status: 400 }
        );
      }
    }

    // Get AI backend URL from environment or use default
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';
    
    console.log('Making request to AI backend:', AI_BACKEND_URL);
    console.log('Request body:', body);

    // Make request to Python AI backend
    const response = await fetch(`${AI_BACKEND_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('AI backend error:', response.status, response.statusText);
      
      // Try to get error details from response
      let errorMessage = `AI backend error: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.detail || errorMessage;
      } catch {
        // If response is not JSON, use status text
        errorMessage = response.statusText || errorMessage;
      }

      return NextResponse.json(
        { error: errorMessage },
        { status: response.status }
      );
    }

    const result: PredictionResponse = await response.json();
    
    console.log('AI backend response:', result);

    // Validate response structure
    if (!result.recommended_crop) {
      return NextResponse.json(
        { error: 'Invalid response from AI backend: missing recommended_crop' },
        { status: 500 }
      );
    }

    // Add timestamp if not present
    if (!result.timestamp) {
      result.timestamp = new Date().toISOString();
    }

    return NextResponse.json(result);

  } catch (error) {
    console.error('Prediction API error:', error);
    
    // Handle specific error types
    if (error instanceof SyntaxError) {
      return NextResponse.json(
        { error: 'Invalid JSON in request body' },
        { status: 400 }
      );
    }

    if (error instanceof TypeError && error.message.includes('fetch')) {
      return NextResponse.json(
        { error: 'Unable to connect to AI backend. Please ensure the AI service is running.' },
        { status: 503 }
      );
    }

    return NextResponse.json(
      { error: 'Internal server error during prediction' },
      { status: 500 }
    );
  }
}

// Handle OPTIONS for CORS if needed
export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}