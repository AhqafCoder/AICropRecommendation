import Header from "@/components/Header";
import Footer from "@/components/Footer";
import CropRecommendationForm from "@/components/CropRecommendationForm";
import { Leaf, Brain, Target } from "lucide-react";

export default function CropRecommendationPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Page Header */}
      <section className="bg-gradient-to-r from-green-600 to-emerald-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/20 text-white text-sm font-medium mb-6">
              <Brain className="w-4 h-4 mr-2" />
              AI-Powered Analysis
            </div>
            <h1 className="text-4xl sm:text-5xl font-bold mb-4">
              Get Personalized Crop Recommendations
            </h1>
            <p className="text-xl text-green-100 max-w-3xl mx-auto">
              Our advanced AI analyzes your soil conditions, climate data, and farming history 
              to recommend the most profitable crops for your land.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="space-y-3">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <Brain className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">AI-Powered Analysis</h3>
              <p className="text-gray-600">
                Advanced machine learning models analyze soil, weather, and historical data
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <Target className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Personalized Results</h3>
              <p className="text-gray-600">
                Recommendations tailored to your specific field conditions and region
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <Leaf className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Profit Optimization</h3>
              <p className="text-gray-600">
                Maximize your returns with yield predictions and cost analysis
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Form */}
      <main className="py-8">
        <CropRecommendationForm />
      </main>

      <Footer />
    </div>
  );
}
