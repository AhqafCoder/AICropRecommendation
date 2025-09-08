"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Leaf, TrendingUp, Sprout, AlertCircle } from "lucide-react";
import { CropAIService, CropPredictionRequest, CropPredictionResponse, validateSoilData, formatCurrency, formatNumber } from "@/lib/api";

export default function CropRecommendationForm() {
  const [formData, setFormData] = useState<Partial<CropPredictionRequest>>({
    N: 90,
    P: 42,
    K: 43,
    temperature: 20.5,
    humidity: 82,
    ph: 6.5,
    rainfall: 200,
    area_ha: 1.0,
    previous_crop: "",
    region: "default",
    season: "kharif"
  });

  const [prediction, setPrediction] = useState<CropPredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (field: keyof CropPredictionRequest, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: field === 'previous_crop' || field === 'region' || field === 'season' ? value : parseFloat(value) || 0
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form data
    const validationErrors = validateSoilData(formData);
    if (validationErrors.length > 0) {
      setError(validationErrors.join(', '));
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await CropAIService.getCropRecommendation(formData as CropPredictionRequest);
      setPrediction(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Leaf className="w-5 h-5 text-green-600" />
              Soil & Environmental Data
            </CardTitle>
            <CardDescription>
              Enter your field's soil and environmental conditions to get AI-powered crop recommendations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* NPK Values */}
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nitrogen (N) <span className="text-xs text-gray-500">0-200</span>
                  </label>
                  <input
                    type="number"
                    value={formData.N || ''}
                    onChange={(e) => handleInputChange('N', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="90"
                    min="0"
                    max="200"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phosphorus (P) <span className="text-xs text-gray-500">0-150</span>
                  </label>
                  <input
                    type="number"
                    value={formData.P || ''}
                    onChange={(e) => handleInputChange('P', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="42"
                    min="0"
                    max="150"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Potassium (K) <span className="text-xs text-gray-500">0-200</span>
                  </label>
                  <input
                    type="number"
                    value={formData.K || ''}
                    onChange={(e) => handleInputChange('K', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="43"
                    min="0"
                    max="200"
                    step="0.1"
                  />
                </div>
              </div>

              {/* Environmental Conditions */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Temperature (°C) <span className="text-xs text-gray-500">-10 to 55</span>
                  </label>
                  <input
                    type="number"
                    value={formData.temperature || ''}
                    onChange={(e) => handleInputChange('temperature', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="20.5"
                    min="-10"
                    max="55"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Humidity (%) <span className="text-xs text-gray-500">0-100</span>
                  </label>
                  <input
                    type="number"
                    value={formData.humidity || ''}
                    onChange={(e) => handleInputChange('humidity', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="82"
                    min="0"
                    max="100"
                    step="0.1"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Soil pH <span className="text-xs text-gray-500">3.5-9.0</span>
                  </label>
                  <input
                    type="number"
                    value={formData.ph || ''}
                    onChange={(e) => handleInputChange('ph', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="6.5"
                    min="3.5"
                    max="9.0"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Rainfall (mm) <span className="text-xs text-gray-500">0-5000</span>
                  </label>
                  <input
                    type="number"
                    value={formData.rainfall || ''}
                    onChange={(e) => handleInputChange('rainfall', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="200"
                    min="0"
                    max="5000"
                    step="0.1"
                  />
                </div>
              </div>

              {/* Additional Fields */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Area (hectares)
                  </label>
                  <input
                    type="number"
                    value={formData.area_ha || ''}
                    onChange={(e) => handleInputChange('area_ha', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="1.0"
                    min="0.1"
                    max="1000"
                    step="0.1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Previous Crop (optional)
                  </label>
                  <input
                    type="text"
                    value={formData.previous_crop || ''}
                    onChange={(e) => handleInputChange('previous_crop', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                    placeholder="wheat, rice, cotton..."
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Region
                  </label>
                  <select
                    value={formData.region || 'default'}
                    onChange={(e) => handleInputChange('region', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="default">Default</option>
                    <option value="north_india">North India</option>
                    <option value="south_india">South India</option>
                    <option value="west_india">West India</option>
                    <option value="east_india">East India</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Season
                  </label>
                  <select
                    value={formData.season}
                    onChange={(e) => handleInputChange('season', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="kharif">Kharif (Monsoon)</option>
                    <option value="rabi">Rabi (Winter)</option>
                    <option value="zaid">Zaid (Summer)</option>
                  </select>
                </div>
              </div>

              {error && (
                <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-md">
                  <AlertCircle className="w-4 h-4 text-red-600" />
                  <span className="text-red-700 text-sm">{error}</span>
                </div>
              )}

              <Button 
                type="submit" 
                className="w-full bg-green-600 hover:bg-green-700"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sprout className="w-4 h-4 mr-2" />
                    Get Crop Recommendation
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results */}
        <div className="space-y-6">
          {prediction && (
            <>
              {/* Main Recommendation */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sprout className="w-5 h-5 text-green-600" />
                    Recommended Crop
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center space-y-4">
                    <div className="text-3xl font-bold text-green-600 capitalize">
                      {prediction.recommended_crop}
                    </div>
                    <Badge className="bg-green-100 text-green-800">
                      {Math.round(prediction.confidence * 100)}% Confidence
                    </Badge>
                    <div className="text-lg font-medium text-gray-700">
                      Expected Yield: {formatNumber(prediction.expected_yield_t_per_acre)} tons/acre
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Explanations */}
              <Card>
                <CardHeader>
                  <CardTitle>Why This Crop?</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {prediction.why.map((reason, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{reason}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Profit Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    Profit Analysis
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Gross Revenue:</span>
                      <span className="font-medium text-green-600">
                        {formatCurrency(prediction.profit_breakdown.gross)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Investment:</span>
                      <span className="font-medium text-red-600">
                        {formatCurrency(prediction.profit_breakdown.investment)}
                      </span>
                    </div>
                    <div className="border-t pt-2">
                      <div className="flex justify-between">
                        <span className="font-medium">Net Profit:</span>
                        <span className="font-bold text-green-600">
                          {formatCurrency(prediction.profit_breakdown.net)}
                        </span>
                      </div>
                      <div className="flex justify-between text-sm text-gray-600">
                        <span>ROI:</span>
                        <span>{formatNumber(prediction.profit_breakdown.roi)}%</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Fertilizer Recommendation */}
              <Card>
                <CardHeader>
                  <CardTitle>Fertilizer Recommendation</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Type:</span>
                      <span className="font-medium">{prediction.fertilizer_recommendation.type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Dosage:</span>
                      <span className="font-medium">
                        {formatNumber(prediction.fertilizer_recommendation.dosage_kg_per_ha)} kg/ha
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Cost:</span>
                      <span className="font-medium text-green-600">
                        {formatCurrency(prediction.fertilizer_recommendation.cost)}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Season Analysis */}
              {prediction.season_analysis && (
                <Card>
                  <CardHeader>
                    <CardTitle>Season Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Detected Season:</span>
                        <Badge className="capitalize">
                          {prediction.season_analysis.detected_season}
                        </Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Suitability:</span>
                        <span className="font-medium">{prediction.season_analysis.season_suitability}</span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2">
                        {prediction.season_analysis.season_explanation}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          )}

          {!prediction && !loading && (
            <Card>
              <CardContent className="text-center py-8">
                <Leaf className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">
                  Fill in your soil and environmental data to get AI-powered crop recommendations
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
