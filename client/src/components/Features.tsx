"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Brain, 
  Camera, 
  Globe, 
  ShoppingCart, 
  BarChart3, 
  TrendingUp,
  Leaf,
  Search,
  Users,
  DollarSign,
  Target,
  Zap
} from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI-Powered Crop Recommendation",
    description: "Personalized suggestions for the best crops based on soil, weather, and historical data.",
    badge: "AI-Powered",
    color: "bg-green-100 text-green-800",
    iconColor: "text-green-600"
  },
  {
    icon: Camera,
    title: "Real-Time Disease Detection",
    description: "Utilizing advanced image recognition to identify crop diseases instantly from uploaded photos.",
    badge: "Computer Vision",
    color: "bg-blue-100 text-blue-800",
    iconColor: "text-blue-600"
  },
  {
    icon: Globe,
    title: "Multilingual Accessibility",
    description: "Providing guidance and insights in local languages to ensure broad usability and understanding.",
    badge: "Inclusive",
    color: "bg-purple-100 text-purple-800",
    iconColor: "text-purple-600"
  },
  {
    icon: ShoppingCart,
    title: "Integrated Marketplace",
    description: "Connecting farmers directly to buyers and suppliers, streamlining the selling and sourcing process.",
    badge: "E-Commerce",
    color: "bg-orange-100 text-orange-800",
    iconColor: "text-orange-600"
  },
  {
    icon: BarChart3,
    title: "Smart Analytics Dashboard",
    description: "A personalized hub for farmers to track progress, access historical data, and plan future yields.",
    badge: "Analytics",
    color: "bg-indigo-100 text-indigo-800",
    iconColor: "text-indigo-600"
  },
  {
    icon: TrendingUp,
    title: "Market Insights & Price Trends",
    description: "Real-time market demand and crop pricing data to guide better investment and cultivation decisions.",
    badge: "Market Intelligence",
    color: "bg-emerald-100 text-emerald-800",
    iconColor: "text-emerald-600"
  }
];

export default function Features() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <Badge className="mb-4 bg-green-100 text-green-800 hover:bg-green-100">
            <Leaf className="w-4 h-4 mr-1" />
            Features
          </Badge>
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            Comprehensive Agricultural Solutions
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our platform combines cutting-edge AI technology with practical farming insights 
            to revolutionize agricultural decision-making.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <Card 
                key={index} 
                className="relative overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 bg-gradient-to-br from-white to-gray-50"
              >
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-3">
                    <div className={`p-3 rounded-full bg-gradient-to-r ${feature.iconColor === 'text-green-600' ? 'from-green-100 to-green-200' : 
                      feature.iconColor === 'text-blue-600' ? 'from-blue-100 to-blue-200' :
                      feature.iconColor === 'text-purple-600' ? 'from-purple-100 to-purple-200' :
                      feature.iconColor === 'text-orange-600' ? 'from-orange-100 to-orange-200' :
                      feature.iconColor === 'text-indigo-600' ? 'from-indigo-100 to-indigo-200' :
                      'from-emerald-100 to-emerald-200'}`}>
                      <IconComponent className={`w-6 h-6 ${feature.iconColor}`} />
                    </div>
                    <Badge className={feature.color}>
                      {feature.badge}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg font-semibold text-gray-900 leading-tight">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardContent>
                
                {/* Decorative Element */}
                <div className="absolute -bottom-2 -right-2 w-20 h-20 bg-gradient-to-br from-green-100 to-green-200 rounded-full opacity-20"></div>
              </Card>
            );
          })}
        </div>

        {/* Additional Info Section */}
        <div className="mt-16 text-center">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            <div className="flex flex-col items-center">
              <Target className="w-8 h-8 text-green-600 mb-2" />
              <div className="text-sm font-medium text-gray-900">Precision Farming</div>
            </div>
            <div className="flex flex-col items-center">
              <Zap className="w-8 h-8 text-green-600 mb-2" />
              <div className="text-sm font-medium text-gray-900">Real-Time Processing</div>
            </div>
            <div className="flex flex-col items-center">
              <Users className="w-8 h-8 text-green-600 mb-2" />
              <div className="text-sm font-medium text-gray-900">Community Driven</div>
            </div>
            <div className="flex flex-col items-center">
              <DollarSign className="w-8 h-8 text-green-600 mb-2" />
              <div className="text-sm font-medium text-gray-900">Cost Effective</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
