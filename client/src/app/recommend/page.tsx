"use client";

import { useState } from 'react';
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { CustomSelect } from '@/components/ui/custom-select';
import { 
  Leaf, TrendingUp, DollarSign, Droplets, Thermometer, Gauge, 
  Brain, Target, Sprout, BarChart3, PieChart, Activity,
  Loader2, AlertCircle, CheckCircle, Info
} from 'lucide-react';
import { PieChart as RechartsPieChart, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line, Area, AreaChart, Pie } from 'recharts';

interface PredictionResult {
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
}

export default function CropRecommendationPage() {
  const [formData, setFormData] = useState({
    N: 60,
    P: 45,
    K: 50,
    temperature: 25,
    humidity: 70,
    ph: 6.5,
    rainfall: 800,
    area_ha: 2.0,
    region: 'default',
    previous_crop: '',
    season: 'auto-detect',
    planting_date: new Date().toISOString().split('T')[0]
  });

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (name: string, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const loadExample = (exampleName: string) => {
    const examples = {
      "Rice Farm (Kharif)": {
        N: 80, P: 40, K: 40, temperature: 27, humidity: 80,
        ph: 6.0, rainfall: 1200, area_ha: 3.0, season: "kharif"
      },
      "Wheat Farm (Rabi)": {
        N: 120, P: 60, K: 40, temperature: 20, humidity: 65,
        ph: 7.5, rainfall: 300, area_ha: 5.0, season: "rabi"
      },
      "Cotton Farm": {
        N: 90, P: 50, K: 50, temperature: 30, humidity: 70,
        ph: 7.0, rainfall: 600, area_ha: 10.0, season: "kharif"
      },
      "Vegetable Farm": {
        N: 100, P: 80, K: 60, temperature: 25, humidity: 75,
        ph: 6.5, rainfall: 500, area_ha: 1.0, season: "auto-detect"
      }
    };

    const example = examples[exampleName as keyof typeof examples];
    if (example) {
      setFormData(prev => ({ ...prev, ...example }));
    }
  };

  const generatePrediction = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          planting_date: formData.season === 'auto-detect' ? formData.planting_date : ''
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.error) {
        throw new Error(result.error);
      }

      setPrediction(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };

  // Chart data preparation
  const npkData = [
    { name: 'Nitrogen (N)', value: formData.N, color: '#3B82F6' },
    { name: 'Phosphorus (P)', value: formData.P, color: '#10B981' },
    { name: 'Potassium (K)', value: formData.K, color: '#F59E0B' },
  ];

  const climateData = [
    { name: 'Temperature', value: formData.temperature, unit: '°C', optimal: 25 },
    { name: 'Humidity', value: formData.humidity, unit: '%', optimal: 70 },
    { name: 'pH Level', value: formData.ph, unit: '', optimal: 6.5 },
    { name: 'Rainfall', value: formData.rainfall, unit: 'mm', optimal: 800 },
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <Header />
      
      {/* Enhanced Hero Section */}
      <section className="bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="inline-flex items-center px-6 py-3 rounded-full bg-white/20 backdrop-blur-sm text-white text-sm font-medium mb-6">
              <Brain className="w-5 h-5 mr-2" />
              AI-Powered Precision Agriculture
            </div>
            <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-green-100">
              Smart Crop Recommendations
            </h1>
            <p className="text-xl text-green-100 max-w-4xl mx-auto mb-8">
              Leverage advanced machine learning and real-time data analysis to optimize your farming decisions, 
              maximize yields, and boost profitability with personalized crop recommendations.
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="flex items-center bg-white/10 backdrop-blur-sm rounded-full px-4 py-2">
                <CheckCircle className="w-4 h-4 mr-2" />
                97% Accuracy Rate
              </div>
              <div className="flex items-center bg-white/10 backdrop-blur-sm rounded-full px-4 py-2">
                <TrendingUp className="w-4 h-4 mr-2" />
                25% Avg. ROI Increase
              </div>
              <div className="flex items-center bg-white/10 backdrop-blur-sm rounded-full px-4 py-2">
                <Leaf className="w-4 h-4 mr-2" />
                20+ Crop Types
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Features Grid */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose Our AI Platform?</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Advanced algorithms meet agricultural expertise to deliver unprecedented farming insights
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: Brain,
                title: "AI-Powered Analysis",
                description: "Machine learning models trained on millions of agricultural data points",
                color: "blue"
              },
              {
                icon: Target,
                title: "Precision Targeting",
                description: "Personalized recommendations based on your specific soil and climate conditions",
                color: "green"
              },
              {
                icon: BarChart3,
                title: "Profit Optimization",
                description: "Detailed financial analysis with ROI predictions and cost breakdowns",
                color: "purple"
              },
              {
                icon: Activity,
                title: "Real-time Insights",
                description: "Live data integration for up-to-date recommendations and market trends",
                color: "orange"
              }
            ].map((feature, index) => (
              <Card key={index} className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                <CardContent className="p-6">
                  <div className={`w-12 h-12 bg-${feature.color}-100 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className={`w-6 h-6 text-${feature.color}-600`} />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600 text-sm">{feature.description}</p>
                </CardContent>
                <div className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-${feature.color}-400 to-${feature.color}-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300`}></div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Enhanced Main Application */}
      <main className="py-12 bg-gradient-to-b from-gray-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-3 gap-8">
            
            {/* Enhanced Input Panel */}
            <div className="lg:col-span-1 space-y-6">
              <Card className="border-0 shadow-lg">
                <CardHeader className="bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-t-lg">
                  <CardTitle className="flex items-center gap-3">
                    <Leaf className="h-6 w-6" />
                    Farm Parameters
                  </CardTitle>
                  <CardDescription className="text-green-100">
                    Enter your field conditions for AI analysis
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-6 space-y-6">
                  
                  {/* Soil Nutrients with Visual Indicators */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 mb-3">
                      <Sprout className="h-5 w-5 text-green-600" />
                      <h3 className="font-semibold text-gray-900">Soil Nutrients (kg/ha)</h3>
                    </div>
                    
                    <div className="grid grid-cols-1 gap-4">
                      {[
                        { key: 'N', label: 'Nitrogen (N)', max: 200, color: 'blue', icon: '🟦' },
                        { key: 'P', label: 'Phosphorus (P)', max: 150, color: 'green', icon: '🟩' },
                        { key: 'K', label: 'Potassium (K)', max: 200, color: 'yellow', icon: '🟨' }
                      ].map((nutrient) => (
                        <div key={nutrient.key} className="space-y-3 p-4 border border-gray-200 rounded-lg bg-gray-50/50 hover:bg-gray-50 transition-colors">
                          <div className="flex items-center justify-between">
                            <Label className="flex items-center gap-2 text-sm font-medium">
                              <span className="text-lg">{nutrient.icon}</span>
                              {nutrient.label}
                            </Label>
                            <Badge variant="outline" className={`font-semibold`}>
                              {formData[nutrient.key as keyof typeof formData]} kg/ha
                            </Badge>
                          </div>
                          <Input
                            type="number"
                            min="0"
                            max={nutrient.max}
                            value={formData[nutrient.key as keyof typeof formData]}
                            onChange={(e) => handleInputChange(nutrient.key, parseFloat(e.target.value))}
                            className="w-full transition-all duration-200 focus:ring-2 focus:ring-blue-500/20 border-2"
                          />
                          <div className="flex justify-between text-xs text-gray-500">
                            <span>Min: 0</span>
                            <span>Max: {nutrient.max}</span>
                          </div>
                          <Progress 
                            value={(Number(formData[nutrient.key as keyof typeof formData]) / nutrient.max) * 100} 
                            className="h-3" 
                          />
                          <div className="text-xs text-center text-gray-600 font-medium">
                            {((Number(formData[nutrient.key as keyof typeof formData]) / nutrient.max) * 100).toFixed(0)}% of maximum
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <Separator />

                  {/* Climate Conditions with Icons */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 mb-3">
                      <Thermometer className="h-5 w-5 text-orange-600" />
                      <h3 className="font-semibold text-gray-900">Climate Conditions</h3>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <Thermometer className="h-4 w-4 text-orange-500" />
                          Temperature (°C)
                        </Label>
                        <Input
                          type="number"
                          min="-10"
                          max="55"
                          step="0.5"
                          value={formData.temperature}
                          onChange={(e) => handleInputChange('temperature', parseFloat(e.target.value))}
                          className="transition-all duration-200 focus:ring-2 focus:ring-orange-500/20"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>Min: -10°C</span>
                          <span>Max: 55°C</span>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <Droplets className="h-4 w-4 text-blue-500" />
                          Humidity (%)
                        </Label>
                        <Input
                          type="number"
                          min="0"
                          max="100"
                          value={formData.humidity}
                          onChange={(e) => handleInputChange('humidity', parseFloat(e.target.value))}
                          className="transition-all duration-200 focus:ring-2 focus:ring-blue-500/20"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>Min: 0%</span>
                          <span>Max: 100%</span>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <Gauge className="h-4 w-4 text-purple-500" />
                          pH Level
                        </Label>
                        <Input
                          type="number"
                          min="3.5"
                          max="9.0"
                          step="0.1"
                          value={formData.ph}
                          onChange={(e) => handleInputChange('ph', parseFloat(e.target.value))}
                          className="transition-all duration-200 focus:ring-2 focus:ring-purple-500/20"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>Acidic: 3.5</span>
                          <span>Alkaline: 9.0</span>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <Droplets className="h-4 w-4 text-cyan-500" />
                          Rainfall (mm)
                        </Label>
                        <Input
                          type="number"
                          min="0"
                          max="5000"
                          value={formData.rainfall}
                          onChange={(e) => handleInputChange('rainfall', parseFloat(e.target.value))}
                          className="transition-all duration-200 focus:ring-2 focus:ring-cyan-500/20"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>Arid: 0mm</span>
                          <span>Tropical: 5000mm</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <Separator />

                  {/* Enhanced Advanced Parameters */}
                  <div className="space-y-4">
                    <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                      <Target className="h-5 w-5 text-indigo-600" />
                      Advanced Parameters
                    </h3>
                    
                    <div className="space-y-6">
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <span className="text-lg">🌾</span>
                          Farm Area (hectares)
                        </Label>
                        <Input
                          type="number"
                          min="0.1"
                          max="1000"
                          step="0.1"
                          value={formData.area_ha}
                          onChange={(e) => handleInputChange('area_ha', parseFloat(e.target.value))}
                          className="transition-all duration-200 focus:ring-2 focus:ring-indigo-500/20 border-2"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                          <span>Min: 0.1 ha</span>
                          <span>Max: 1000 ha</span>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <span className="text-lg">🗺️</span>
                          Region
                        </Label>
                        <CustomSelect 
                          value={formData.region} 
                          onChange={(e) => handleInputChange('region', e.target.value)}
                          className="border-2 transition-all duration-200 focus:ring-2 focus:ring-indigo-500/20"
                        >
                          <option value="default">Default</option>
                          <option value="north">North India</option>
                          <option value="south">South India</option>
                          <option value="east">East India</option>
                          <option value="west">West India</option>
                          <option value="central">Central India</option>
                        </CustomSelect>
                      </div>
                      
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <span className="text-lg">🌱</span>
                          Previous Crop (Optional)
                        </Label>
                        <CustomSelect 
                          value={formData.previous_crop} 
                          onChange={(e) => handleInputChange('previous_crop', e.target.value)}
                          className="border-2 transition-all duration-200 focus:ring-2 focus:ring-green-500/20"
                        >
                          <option value="">None</option>
                          <option value="rice">🌾 Rice</option>
                          <option value="wheat">🌾 Wheat</option>
                          <option value="maize">🌽 Maize</option>
                          <option value="cotton">🌿 Cotton</option>
                          <option value="sugarcane">🎋 Sugarcane</option>
                          <option value="banana">🍌 Banana</option>
                          <option value="mango">🥭 Mango</option>
                          <option value="apple">🍎 Apple</option>
                          <option value="grapes">🍇 Grapes</option>
                          <option value="orange">🍊 Orange</option>
                        </CustomSelect>
                      </div>
                      
                      <div className="space-y-2">
                        <Label className="flex items-center gap-2 text-sm font-medium">
                          <span className="text-lg">🌤️</span>
                          Season
                        </Label>
                        <CustomSelect 
                          value={formData.season} 
                          onChange={(e) => handleInputChange('season', e.target.value)}
                          className="border-2 transition-all duration-200 focus:ring-2 focus:ring-blue-500/20"
                        >
                          <option value="auto-detect">🤖 Auto-detect</option>
                          <option value="kharif">🌧️ Kharif (Monsoon)</option>
                          <option value="rabi">❄️ Rabi (Winter)</option>
                          <option value="zaid">☀️ Zaid (Summer)</option>
                        </CustomSelect>
                      </div>

                      {formData.season === 'auto-detect' && (
                        <div className="space-y-2 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                          <Label className="flex items-center gap-2 text-sm font-medium">
                            <span className="text-lg">📅</span>
                            Planting Date
                          </Label>
                          <Input
                            type="date"
                            value={formData.planting_date}
                            onChange={(e) => handleInputChange('planting_date', e.target.value)}
                            className="transition-all duration-200 focus:ring-2 focus:ring-blue-500/20 border-2"
                          />
                          <p className="text-xs text-blue-600">
                            This helps us auto-detect the optimal season for your crop
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  <Separator />

                  {/* Enhanced Quick Examples */}
                  <div className="space-y-4">
                    <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                      <span className="text-lg">⚡</span>
                      Quick Examples
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {[
                        { name: 'Rice Farm (Kharif)', icon: '🌾', color: 'green' },
                        { name: 'Wheat Farm (Rabi)', icon: '🌾', color: 'yellow' },
                        { name: 'Cotton Farm', icon: '🌿', color: 'blue' },
                        { name: 'Vegetable Farm', icon: '🥬', color: 'emerald' }
                      ].map((example) => (
                        <Button
                          key={example.name}
                          variant="outline"
                          size="sm"
                          onClick={() => loadExample(example.name)}
                          className={`text-xs h-10 hover:bg-${example.color}-50 hover:border-${example.color}-300 transition-all duration-200 flex items-center gap-2`}
                        >
                          <span className="text-sm">{example.icon}</span>
                          {example.name}
                        </Button>
                      ))}
                    </div>
                  </div>

                  {/* Enhanced Generate Button */}
                  <div className="pt-4">
                    <Button
                      onClick={generatePrediction}
                      disabled={loading}
                      className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-semibold py-4 text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-[1.02]"
                      size="lg"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="mr-3 h-5 w-5 animate-spin" />
                          <span>Analyzing your farm data...</span>
                        </>
                      ) : (
                        <>
                          <Brain className="mr-3 h-5 w-5" />
                          <span>Get AI Recommendation</span>
                        </>
                      )}
                    </Button>
                    <p className="text-xs text-center text-gray-500 mt-2">
                      Powered by advanced machine learning algorithms
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Enhanced Input Visualization */}
              <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-t-lg">
                  <CardTitle className="flex items-center gap-2">
                    <PieChart className="h-5 w-5" />
                    NPK Nutrient Analysis
                  </CardTitle>
                  <CardDescription className="text-blue-100">
                    Real-time visualization of your soil nutrients
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <RechartsPieChart>
                        <Pie
                          data={npkData}
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={90}
                          dataKey="value"
                          label={({ name, value }) => `${name}: ${value}`}
                        >
                          {npkData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value, name) => [`${value} kg/ha`, name]} />
                      </RechartsPieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="mt-4 space-y-2">
                    {npkData.map((nutrient, index) => (
                      <div key={index} className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2">
                          <div 
                            className="w-3 h-3 rounded-full" 
                            style={{ backgroundColor: nutrient.color }}
                          ></div>
                          <span className="font-medium">{nutrient.name}</span>
                        </div>
                        <span className="text-gray-600">{nutrient.value} kg/ha</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Enhanced Results Panel */}
            <div className="lg:col-span-2 space-y-6">
              {loading && (
                <Card className="border-2 border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50">
                  <CardContent className="flex flex-col items-center justify-center py-16 text-center">
                    <div className="relative">
                      <div className="w-20 h-20 border-4 border-blue-200 rounded-full"></div>
                      <div className="w-20 h-20 border-4 border-blue-600 border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
                    </div>
                    <div className="mt-6">
                      <h3 className="text-xl font-semibold text-blue-800 mb-2">Analyzing Your Farm Data</h3>
                      <p className="text-blue-600 max-w-md">
                        Our AI is processing your soil and climate parameters to generate personalized crop recommendations...
                      </p>
                      <div className="mt-4 flex flex-wrap gap-2 justify-center">
                        <Badge className="bg-blue-100 text-blue-800">🧠 AI Processing</Badge>
                        <Badge className="bg-green-100 text-green-800">📊 Data Analysis</Badge>
                        <Badge className="bg-purple-100 text-purple-800">💰 Profit Calculation</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {error && (
                <Card className="border-2 border-red-200 bg-gradient-to-br from-red-50 to-pink-50">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className="flex-shrink-0">
                      <AlertCircle className="h-8 w-8 text-red-600" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-red-800 mb-1">Analysis Failed</h3>
                      <p className="text-red-700 mb-3">{error}</p>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => setError(null)}
                        className="border-red-300 text-red-700 hover:bg-red-50"
                      >
                        Try Again
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )}

              {prediction ? (
                <Card className="border-0 shadow-xl">
                  <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg">
                    <CardTitle className="flex items-center gap-3 text-xl">
                      <TrendingUp className="h-6 w-6" />
                      AI Prediction Results
                    </CardTitle>
                    <CardDescription className="text-blue-100">
                      Comprehensive analysis based on your farm parameters
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-0">
                    <Tabs defaultValue="overview" className="w-full">
                      <TabsList className="grid w-full grid-cols-5 bg-gray-50 rounded-none">
                        <TabsTrigger value="overview" className="flex items-center gap-2">
                          <Info className="h-4 w-4" />
                          Overview
                        </TabsTrigger>
                        <TabsTrigger value="financial" className="flex items-center gap-2">
                          <DollarSign className="h-4 w-4" />
                          Financial
                        </TabsTrigger>
                        <TabsTrigger value="analysis" className="flex items-center gap-2">
                          <BarChart3 className="h-4 w-4" />
                          Analysis
                        </TabsTrigger>
                        <TabsTrigger value="recommendations" className="flex items-center gap-2">
                          <Target className="h-4 w-4" />
                          Recommendations
                        </TabsTrigger>
                        <TabsTrigger value="insights" className="flex items-center gap-2">
                          <Brain className="h-4 w-4" />
                          AI Insights
                        </TabsTrigger>
                      </TabsList>

                      {/* Overview Tab */}
                      <TabsContent value="overview" className="p-6 space-y-6">
                        {/* Key Metrics Cards */}
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                          <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
                            <CardContent className="p-4 text-center">
                              <Leaf className="h-8 w-8 text-green-600 mx-auto mb-2" />
                              <p className="text-sm font-medium text-green-800">Recommended Crop</p>
                              <p className="text-2xl font-bold text-green-700 capitalize">
                                {prediction.recommended_crop}
                              </p>
                            </CardContent>
                          </Card>
                          
                          <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
                            <CardContent className="p-4 text-center">
                              <Gauge className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                              <p className="text-sm font-medium text-blue-800">Confidence</p>
                              <p className="text-2xl font-bold text-blue-700">
                                {(prediction.confidence * 100).toFixed(1)}%
                              </p>
                              <Progress value={prediction.confidence * 100} className="mt-2" />
                            </CardContent>
                          </Card>
                          
                          <Card className="bg-gradient-to-br from-purple-50 to-violet-50 border-purple-200">
                            <CardContent className="p-4 text-center">
                              <TrendingUp className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                              <p className="text-sm font-medium text-purple-800">Expected Yield</p>
                              <p className="text-2xl font-bold text-purple-700">
                                {prediction.expected_yield_t_per_acre.toFixed(1)}
                              </p>
                              <p className="text-xs text-purple-600">tonnes/acre</p>
                            </CardContent>
                          </Card>
                          
                          <Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
                            <CardContent className="p-4 text-center">
                              <DollarSign className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                              <p className="text-sm font-medium text-orange-800">Net Profit</p>
                              <p className="text-2xl font-bold text-orange-700">
                                ₹{(prediction.profit_breakdown.net / 1000).toFixed(0)}K
                              </p>
                              <p className="text-xs text-orange-600">
                                {prediction.profit_breakdown.roi.toFixed(1)}% ROI
                              </p>
                            </CardContent>
                          </Card>
                        </div>

                        {/* Yield Range Visualization */}
                        <Card>
                          <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                              <BarChart3 className="h-5 w-5 text-green-600" />
                              Yield Prediction Range
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-4">
                              <div className="flex justify-between items-center">
                                <span className="text-sm font-medium">Low Estimate (P10)</span>
                                <Badge variant="outline">{prediction.yield_interval_p10_p90[0].toFixed(1)} t/acre</Badge>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-sm font-medium">Expected Yield</span>
                                <Badge className="bg-green-600">{prediction.expected_yield_t_per_acre.toFixed(1)} t/acre</Badge>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-sm font-medium">High Estimate (P90)</span>
                                <Badge variant="outline">{prediction.yield_interval_p10_p90[1].toFixed(1)} t/acre</Badge>
                              </div>
                              <div className="mt-4">
                                <div className="h-4 bg-gray-200 rounded-full relative">
                                  <div 
                                    className="h-full bg-gradient-to-r from-green-400 to-green-600 rounded-full"
                                    style={{
                                      width: `${(prediction.expected_yield_t_per_acre / prediction.yield_interval_p10_p90[1]) * 100}%`
                                    }}
                                  ></div>
                                </div>
                                <div className="flex justify-between text-xs text-gray-500 mt-1">
                                  <span>{prediction.yield_interval_p10_p90[0].toFixed(1)}</span>
                                  <span>{prediction.yield_interval_p10_p90[1].toFixed(1)}</span>
                                </div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </TabsContent>

                      {/* Financial Tab with Charts */}
                      <TabsContent value="financial" className="p-6 space-y-6">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                          {/* Profit Breakdown Pie Chart */}
                          <Card>
                            <CardHeader>
                              <CardTitle className="flex items-center gap-2">
                                <PieChart className="h-5 w-5 text-blue-600" />
                                Financial Breakdown
                              </CardTitle>
                            </CardHeader>
                            <CardContent>
                              <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                  <RechartsPieChart>
                                    <Pie
                                      data={[
                                        { name: 'Net Profit', value: prediction.profit_breakdown.net, color: '#10B981' },
                                        { name: 'Investment', value: prediction.profit_breakdown.investment, color: '#EF4444' }
                                      ]}
                                      cx="50%"
                                      cy="50%"
                                      innerRadius={60}
                                      outerRadius={100}
                                      dataKey="value"
                                      label={({ name, value }) => `${name}: ₹${value ? (Number(value)/1000).toFixed(0) : '0'}K`}
                                    >
                                      <Cell fill="#10B981" />
                                      <Cell fill="#EF4444" />
                                    </Pie>
                                    <Tooltip formatter={(value) => `₹${Number(value).toLocaleString()}`} />
                                  </RechartsPieChart>
                                </ResponsiveContainer>
                              </div>
                            </CardContent>
                          </Card>

                          {/* Financial Details */}
                          <Card>
                            <CardHeader>
                              <CardTitle>Financial Summary</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                              <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                                <span className="font-medium text-green-800">Gross Revenue</span>
                                <span className="font-bold text-green-700">₹{prediction.profit_breakdown.gross.toLocaleString()}</span>
                              </div>
                              <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                                <span className="font-medium text-red-800">Total Investment</span>
                                <span className="font-bold text-red-700">₹{prediction.profit_breakdown.investment.toLocaleString()}</span>
                              </div>
                              <Separator />
                              <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                                <span className="font-bold text-blue-800">Net Profit</span>
                                <span className="font-bold text-blue-700 text-lg">₹{prediction.profit_breakdown.net.toLocaleString()}</span>
                              </div>
                              <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                                <span className="font-bold text-purple-800">Return on Investment</span>
                                <div className="text-right">
                                  <span className="font-bold text-purple-700 text-lg">{prediction.profit_breakdown.roi.toFixed(1)}%</span>
                                  <Progress value={Math.min(prediction.profit_breakdown.roi, 100)} className="mt-1 w-24" />
                                </div>
                              </div>
                              
                              {/* ROI Indicator */}
                              <div className="mt-4 p-3 rounded-lg" style={{
                                backgroundColor: prediction.profit_breakdown.roi > 50 ? '#DCFCE7' : 
                                                prediction.profit_breakdown.roi > 30 ? '#FEF3C7' : '#FEE2E2'
                              }}>
                                <p className="text-center font-medium" style={{
                                  color: prediction.profit_breakdown.roi > 50 ? '#166534' : 
                                         prediction.profit_breakdown.roi > 30 ? '#92400E' : '#991B1B'
                                }}>
                                  {prediction.profit_breakdown.roi > 50 ? '🎉 Excellent ROI' : 
                                   prediction.profit_breakdown.roi > 30 ? '👍 Good ROI' : 
                                   prediction.profit_breakdown.roi > 15 ? '⚠️ Average ROI' : '⚠️ Low ROI'}
                                </p>
                              </div>
                            </CardContent>
                          </Card>
                        </div>
                      </TabsContent>

                      {/* Analysis Tab */}
                      <TabsContent value="analysis" className="p-6 space-y-6">
                        {prediction.previous_crop_analysis && (
                          <Card>
                            <CardHeader>
                              <CardTitle className="flex items-center gap-2">
                                <BarChart3 className="h-5 w-5 text-orange-600" />
                                Previous Crop Impact Analysis
                              </CardTitle>
                            </CardHeader>
                            <CardContent>
                              <div className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                  <div>
                                    <p className="text-sm font-medium text-gray-600 mb-2">Original NPK Levels</p>
                                    <div className="flex gap-2">
                                      <Badge className="bg-blue-100 text-blue-800">N: {prediction.previous_crop_analysis.original_npk[0]}</Badge>
                                      <Badge className="bg-green-100 text-green-800">P: {prediction.previous_crop_analysis.original_npk[1]}</Badge>
                                      <Badge className="bg-yellow-100 text-yellow-800">K: {prediction.previous_crop_analysis.original_npk[2]}</Badge>
                                    </div>
                                  </div>
                                  <div>
                                    <p className="text-sm font-medium text-gray-600 mb-2">AI-Adjusted NPK Levels</p>
                                    <div className="flex gap-2">
                                      <Badge className="bg-blue-600 text-white">N: {prediction.previous_crop_analysis.adjusted_npk[0]}</Badge>
                                      <Badge className="bg-green-600 text-white">P: {prediction.previous_crop_analysis.adjusted_npk[1]}</Badge>
                                      <Badge className="bg-yellow-600 text-white">K: {prediction.previous_crop_analysis.adjusted_npk[2]}</Badge>
                                    </div>
                                  </div>
                                </div>
                                
                                <div className="p-4 bg-blue-50 rounded-lg">
                                  <p className="text-sm font-medium text-blue-800 mb-1">Nutrient Impact Analysis</p>
                                  <p className="text-blue-700">{prediction.previous_crop_analysis.nutrient_impact}</p>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        )}

                        {prediction.season_analysis && (
                          <Card>
                            <CardHeader>
                              <CardTitle className="flex items-center gap-2">
                                <Activity className="h-5 w-5 text-green-600" />
                                Season Analysis
                              </CardTitle>
                            </CardHeader>
                            <CardContent>
                              <div className="space-y-4">
                                <div className="flex items-center gap-4">
                                  <Badge variant="outline" className="text-lg px-4 py-2">
                                    {prediction.season_analysis.detected_season === 'kharif' ? '🌧️' : 
                                     prediction.season_analysis.detected_season === 'rabi' ? '❄️' : '☀️'}
                                    {prediction.season_analysis.detected_season}
                                  </Badge>
                                  <Badge className={`px-4 py-2 ${
                                    prediction.season_analysis.season_suitability === 'Highly Suitable' ? 'bg-green-600' :
                                    prediction.season_analysis.season_suitability === 'Suitable' ? 'bg-yellow-600' : 'bg-red-600'
                                  }`}>
                                    {prediction.season_analysis.season_suitability}
                                  </Badge>
                                </div>
                                <div className="p-4 bg-green-50 rounded-lg">
                                  <p className="text-green-800">{prediction.season_analysis.season_explanation}</p>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        )}

                        {/* Climate Data Visualization */}
                        <Card>
                          <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                              <Thermometer className="h-5 w-5 text-blue-600" />
                              Climate Parameter Analysis
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="h-64">
                              <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={climateData}>
                                  <CartesianGrid strokeDasharray="3 3" />
                                  <XAxis dataKey="name" />
                                  <YAxis />
                                  <Tooltip />
                                  <Legend />
                                  <Bar dataKey="value" fill="#3B82F6" name="Current Value" />
                                  <Bar dataKey="optimal" fill="#10B981" name="Optimal Value" />
                                </BarChart>
                              </ResponsiveContainer>
                            </div>
                          </CardContent>
                        </Card>
                      </TabsContent>

                      {/* Recommendations Tab */}
                      <TabsContent value="recommendations" className="p-6 space-y-6">
                        {prediction.fertilizer_recommendation && (
                          <Card>
                            <CardHeader>
                              <CardTitle className="flex items-center gap-2">
                                <Sprout className="h-5 w-5 text-green-600" />
                                Fertilizer Recommendations
                              </CardTitle>
                            </CardHeader>
                            <CardContent>
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="p-4 bg-green-50 rounded-lg text-center">
                                  <p className="text-sm font-medium text-green-800">Fertilizer Type</p>
                                  <p className="text-lg font-bold text-green-700">{prediction.fertilizer_recommendation.type}</p>
                                </div>
                                <div className="p-4 bg-blue-50 rounded-lg text-center">
                                  <p className="text-sm font-medium text-blue-800">Dosage</p>
                                  <p className="text-lg font-bold text-blue-700">{prediction.fertilizer_recommendation.dosage_kg_per_ha} kg/ha</p>
                                </div>
                                <div className="p-4 bg-purple-50 rounded-lg text-center">
                                  <p className="text-sm font-medium text-purple-800">Estimated Cost</p>
                                  <p className="text-lg font-bold text-purple-700">₹{prediction.fertilizer_recommendation.cost.toLocaleString()}</p>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        )}

                        {/* Action Items */}
                        <Card>
                          <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                              <CheckCircle className="h-5 w-5 text-green-600" />
                              Recommended Actions
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-3">
                              {[
                                { action: `Plant ${prediction.recommended_crop} for optimal yield`, priority: "high" },
                                { action: "Monitor soil moisture levels regularly", priority: "medium" },
                                { action: "Apply recommended fertilizers before planting", priority: "high" },
                                { action: "Consider crop rotation for next season", priority: "low" },
                                { action: "Set up pest monitoring systems", priority: "medium" }
                              ].map((item, index) => (
                                <div key={index} className="flex items-center gap-3 p-3 border rounded-lg">
                                  <div className={`w-3 h-3 rounded-full ${
                                    item.priority === 'high' ? 'bg-red-500' :
                                    item.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                                  }`}></div>
                                  <span className="flex-1">{item.action}</span>
                                  <Badge variant="outline" className={
                                    item.priority === 'high' ? 'border-red-500 text-red-700' :
                                    item.priority === 'medium' ? 'border-yellow-500 text-yellow-700' : 'border-green-500 text-green-700'
                                  }>
                                    {item.priority}
                                  </Badge>
                                </div>
                              ))}
                            </div>
                          </CardContent>
                        </Card>
                      </TabsContent>

                      {/* AI Insights Tab */}
                      <TabsContent value="insights" className="p-6 space-y-6">
                        {prediction.why && (
                          <Card>
                            <CardHeader>
                              <CardTitle className="flex items-center gap-2">
                                <Brain className="h-5 w-5 text-purple-600" />
                                AI Reasoning & Explanations
                              </CardTitle>
                              <CardDescription>
                                Understand how our AI arrived at this recommendation
                              </CardDescription>
                            </CardHeader>
                            <CardContent>
                              <div className="space-y-3">
                                {prediction.why.map((explanation, index) => (
                                  <div key={index} className="flex gap-3 p-4 bg-purple-50 rounded-lg">
                                    <div className="flex-shrink-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                                      {index + 1}
                                    </div>
                                    <p className="text-purple-800">{explanation}</p>
                                  </div>
                                ))}
                              </div>
                            </CardContent>
                          </Card>
                        )}

                        {/* Model Information */}
                        <Card>
                          <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                              <Info className="h-5 w-5 text-blue-600" />
                              Technical Details
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                              <div>
                                <p className="font-medium text-gray-600">Model Version</p>
                                <p className="text-gray-800">{prediction.model_version}</p>
                              </div>
                              <div>
                                <p className="font-medium text-gray-600">Analysis Time</p>
                                <p className="text-gray-800">{new Date(prediction.timestamp).toLocaleString()}</p>
                              </div>
                              <div>
                                <p className="font-medium text-gray-600">Region</p>
                                <p className="text-gray-800 capitalize">{formData.region}</p>
                              </div>
                              <div>
                                <p className="font-medium text-gray-600">Farm Area</p>
                                <p className="text-gray-800">{formData.area_ha} hectares</p>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                </Card>
              ) : !loading && !error && (
                <Card className="border-dashed border-2 border-gray-300 bg-gradient-to-br from-gray-50 to-green-50">
                  <CardContent className="flex flex-col items-center justify-center py-20 text-center">
                    <div className="w-24 h-24 bg-gradient-to-br from-green-100 to-emerald-100 rounded-full flex items-center justify-center mb-6">
                      <Leaf className="h-12 w-12 text-green-600" />
                    </div>
                    <h3 className="text-2xl font-semibold text-gray-800 mb-3">Ready for AI Analysis</h3>
                    <p className="text-gray-600 max-w-md mb-6">
                      Enter your farm parameters on the left and click "Get AI Recommendation" to receive 
                      personalized crop suggestions with detailed financial analysis.
                    </p>
                    <div className="flex flex-wrap gap-2 justify-center mb-6">
                      <Badge variant="outline" className="bg-white border-green-200 text-green-700">🤖 AI-Powered</Badge>
                      <Badge variant="outline" className="bg-white border-blue-200 text-blue-700">📊 Data-Driven</Badge>
                      <Badge variant="outline" className="bg-white border-purple-200 text-purple-700">💰 Profit-Optimized</Badge>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span>20+ Crop Types</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span>97% Accuracy</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span>Real-time Analysis</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
