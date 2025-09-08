"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { 
  TrendingUp, 
  TrendingDown, 
  BarChart3, 
  PieChart, 
  Calendar,
  MapPin,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Leaf,
  Droplets
} from "lucide-react";

interface CropInsight {
  crop: string;
  demandTrend: 'up' | 'down' | 'stable';
  currentPrice: number;
  projectedPrice: number;
  seasonalFactor: number;
  riskLevel: 'low' | 'medium' | 'high';
  bestRegions: string[];
  optimalPlantingWindow: string;
  marketShare: number;
}

interface WeatherForecast {
  region: string;
  temperature: { min: number; max: number };
  rainfall: number;
  humidity: number;
  outlook: 'favorable' | 'moderate' | 'challenging';
  impact: string;
}

interface ProfitabilityInsight {
  crop: string;
  investmentPerAcre: number;
  expectedRevenuePerAcre: number;
  profitMargin: number;
  paybackPeriod: string;
  riskFactor: number;
}

const cropInsights: CropInsight[] = [
  {
    crop: 'Rice',
    demandTrend: 'up',
    currentPrice: 2100,
    projectedPrice: 2250,
    seasonalFactor: 1.15,
    riskLevel: 'low',
    bestRegions: ['Punjab', 'Haryana', 'West Bengal'],
    optimalPlantingWindow: 'June - July',
    marketShare: 35.2
  },
  {
    crop: 'Cotton',
    demandTrend: 'up',
    currentPrice: 5800,
    projectedPrice: 6200,
    seasonalFactor: 1.25,
    riskLevel: 'medium',
    bestRegions: ['Gujarat', 'Maharashtra', 'Andhra Pradesh'],
    optimalPlantingWindow: 'May - June',
    marketShare: 28.7
  },
  {
    crop: 'Wheat',
    demandTrend: 'stable',
    currentPrice: 2050,
    projectedPrice: 2100,
    seasonalFactor: 1.05,
    riskLevel: 'low',
    bestRegions: ['Punjab', 'Uttar Pradesh', 'Madhya Pradesh'],
    optimalPlantingWindow: 'November - December',
    marketShare: 22.1
  },
  {
    crop: 'Sugarcane',
    demandTrend: 'down',
    currentPrice: 320,
    projectedPrice: 310,
    seasonalFactor: 0.95,
    riskLevel: 'high',
    bestRegions: ['Uttar Pradesh', 'Maharashtra', 'Karnataka'],
    optimalPlantingWindow: 'February - March',
    marketShare: 14.0
  }
];

const weatherForecasts: WeatherForecast[] = [
  {
    region: 'Punjab',
    temperature: { min: 25, max: 35 },
    rainfall: 120,
    humidity: 75,
    outlook: 'favorable',
    impact: 'Ideal for rice cultivation'
  },
  {
    region: 'Gujarat',
    temperature: { min: 28, max: 38 },
    rainfall: 80,
    humidity: 65,
    outlook: 'moderate',
    impact: 'Good for cotton with irrigation'
  },
  {
    region: 'Maharashtra',
    temperature: { min: 22, max: 32 },
    rainfall: 150,
    humidity: 80,
    outlook: 'favorable',
    impact: 'Excellent for multiple crops'
  },
  {
    region: 'Karnataka',
    temperature: { min: 20, max: 30 },
    rainfall: 100,
    humidity: 70,
    outlook: 'challenging',
    impact: 'Requires careful water management'
  }
];

const profitabilityInsights: ProfitabilityInsight[] = [
  {
    crop: 'Cotton',
    investmentPerAcre: 25000,
    expectedRevenuePerAcre: 45000,
    profitMargin: 44.4,
    paybackPeriod: '6 months',
    riskFactor: 0.6
  },
  {
    crop: 'Rice',
    investmentPerAcre: 18000,
    expectedRevenuePerAcre: 28000,
    profitMargin: 35.7,
    paybackPeriod: '4 months',
    riskFactor: 0.3
  },
  {
    crop: 'Wheat',
    investmentPerAcre: 15000,
    expectedRevenuePerAcre: 22000,
    profitMargin: 31.8,
    paybackPeriod: '5 months',
    riskFactor: 0.2
  },
  {
    crop: 'Sugarcane',
    investmentPerAcre: 35000,
    expectedRevenuePerAcre: 48000,
    profitMargin: 27.1,
    paybackPeriod: '12 months',
    riskFactor: 0.8
  }
];

export default function AnalyticsPage() {
  const [selectedTimeframe, setSelectedTimeframe] = useState('3months');

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', { 
      style: 'currency', 
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-red-600" />;
      default: return <BarChart3 className="w-4 h-4 text-yellow-600" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up': return 'text-green-600';
      case 'down': return 'text-red-600';
      default: return 'text-yellow-600';
    }
  };

  const getRiskBadgeVariant = (risk: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (risk) {
      case 'low': return 'default';
      case 'medium': return 'secondary';
      case 'high': return 'destructive';
      default: return 'outline';
    }
  };

  const getOutlookIcon = (outlook: string) => {
    switch (outlook) {
      case 'favorable': return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'moderate': return <Clock className="w-4 h-4 text-yellow-600" />;
      case 'challenging': return <AlertTriangle className="w-4 h-4 text-red-600" />;
      default: return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-white pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Market Analytics & Insights
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Data-driven insights to help you make informed agricultural decisions
          </p>
        </div>

        {/* Timeframe Selection */}
        <div className="flex justify-center mb-8">
          <div className="flex bg-white rounded-lg border p-1">
            {[
              { id: '1month', label: '1 Month' },
              { id: '3months', label: '3 Months' },
              { id: '6months', label: '6 Months' },
              { id: '1year', label: '1 Year' }
            ].map((timeframe) => (
              <Button
                key={timeframe.id}
                variant={selectedTimeframe === timeframe.id ? "default" : "ghost"}
                size="sm"
                onClick={() => setSelectedTimeframe(timeframe.id)}
                className="text-sm"
              >
                {timeframe.label}
              </Button>
            ))}
          </div>
        </div>

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <TrendingUp className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Avg. Price Growth</p>
                  <p className="text-2xl font-bold text-gray-900">+8.7%</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <BarChart3 className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Market Volume</p>
                  <p className="text-2xl font-bold text-gray-900">₹2.4Cr</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <PieChart className="w-6 h-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Best ROI Crop</p>
                  <p className="text-2xl font-bold text-gray-900">Cotton</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Droplets className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Weather Risk</p>
                  <p className="text-2xl font-bold text-gray-900">Low</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Crop Market Insights */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-green-600" />
              Crop Market Analysis
            </CardTitle>
            <CardDescription>
              Current market trends and price projections for major crops
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {cropInsights.map((insight, index) => (
                <div key={index} className="p-4 border rounded-lg bg-white">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-lg text-gray-900">{insight.crop}</h3>
                    <div className="flex items-center gap-2">
                      {getTrendIcon(insight.demandTrend)}
                      <Badge variant={getRiskBadgeVariant(insight.riskLevel)}>
                        {insight.riskLevel} risk
                      </Badge>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Current Price</p>
                      <p className="text-xl font-bold">{formatCurrency(insight.currentPrice)}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Projected Price</p>
                      <p className={`text-xl font-bold ${getTrendColor(insight.demandTrend)}`}>
                        {formatCurrency(insight.projectedPrice)}
                      </p>
                    </div>
                  </div>

                  <div className="mb-3">
                    <p className="text-sm text-gray-600 mb-1">Market Share</p>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-green-600 h-2 rounded-full" 
                        style={{ width: `${insight.marketShare}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">{insight.marketShare}%</p>
                  </div>

                  <div className="text-sm">
                    <p className="text-gray-600 mb-1">
                      <Calendar className="w-4 h-4 inline mr-1" />
                      Optimal Planting: {insight.optimalPlantingWindow}
                    </p>
                    <p className="text-gray-600">
                      <MapPin className="w-4 h-4 inline mr-1" />
                      Best Regions: {insight.bestRegions.join(', ')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Weather Insights */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Droplets className="w-5 h-5 text-blue-600" />
              Regional Weather Outlook
            </CardTitle>
            <CardDescription>
              7-day weather forecast and agricultural impact assessment
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {weatherForecasts.map((forecast, index) => (
                <div key={index} className="p-4 border rounded-lg bg-white">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-lg text-gray-900">{forecast.region}</h3>
                    {getOutlookIcon(forecast.outlook)}
                  </div>

                  <div className="grid grid-cols-3 gap-3 mb-4">
                    <div>
                      <p className="text-xs text-gray-600">Temperature</p>
                      <p className="text-sm font-semibold">
                        {forecast.temperature.min}° - {forecast.temperature.max}°C
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Rainfall</p>
                      <p className="text-sm font-semibold">{forecast.rainfall}mm</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">Humidity</p>
                      <p className="text-sm font-semibold">{forecast.humidity}%</p>
                    </div>
                  </div>

                  <div className="p-3 bg-gray-50 rounded">
                    <p className="text-sm text-gray-700">
                      <strong>Impact:</strong> {forecast.impact}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Profitability Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-yellow-600" />
              Profitability Analysis
            </CardTitle>
            <CardDescription>
              Investment requirements and expected returns by crop type
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4">Crop</th>
                    <th className="text-left py-3 px-4">Investment/Acre</th>
                    <th className="text-left py-3 px-4">Expected Revenue</th>
                    <th className="text-left py-3 px-4">Profit Margin</th>
                    <th className="text-left py-3 px-4">Payback Period</th>
                    <th className="text-left py-3 px-4">Risk Level</th>
                  </tr>
                </thead>
                <tbody>
                  {profitabilityInsights
                    .sort((a, b) => b.profitMargin - a.profitMargin)
                    .map((insight, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4 font-medium">{insight.crop}</td>
                      <td className="py-3 px-4">{formatCurrency(insight.investmentPerAcre)}</td>
                      <td className="py-3 px-4">{formatCurrency(insight.expectedRevenuePerAcre)}</td>
                      <td className="py-3 px-4">
                        <span className="text-green-600 font-semibold">
                          {insight.profitMargin.toFixed(1)}%
                        </span>
                      </td>
                      <td className="py-3 px-4">{insight.paybackPeriod}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                insight.riskFactor < 0.4 ? 'bg-green-500' : 
                                insight.riskFactor < 0.7 ? 'bg-yellow-500' : 'bg-red-500'
                              }`}
                              style={{ width: `${insight.riskFactor * 100}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-600">
                            {insight.riskFactor < 0.4 ? 'Low' : 
                             insight.riskFactor < 0.7 ? 'Medium' : 'High'}
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
      <Footer />
    </>
  );
}
