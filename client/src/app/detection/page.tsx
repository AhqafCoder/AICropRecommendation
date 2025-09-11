import Header from "@/components/Header";
import Footer from "@/components/Footer";
import DiseaseDetectionEnhanced from "@/components/DiseaseDetectionEnhanced";
import { Camera, Zap, Shield,Leaf  } from "lucide-react";

export default function DiseaseDetectionPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Professional Header */}
      <div className="bg-gradient-to-r from-emerald-600 mt-10 via-green-600 to-emerald-700 text-white">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="text-center space-y-4">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/20 text-white text-sm font-medium mb-4">
              <Leaf className="w-4 h-4 mr-2" />
              AI-Powered Agriculture
            </div>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
              Advanced Crop Disease Detection
            </h1>
            <p className="text-xl text-emerald-100 max-w-3xl mx-auto leading-relaxed">
              Upload high-quality images of your crops for instant AI diagnosis, 
              expert recommendations, and comprehensive treatment plans.
            </p>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <section className="py-16 bg-gradient-to-br from-emerald-50 to-green-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
            <div className="space-y-4 p-6 bg-white rounded-xl shadow-lg border border-emerald-100">
              <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-green-600 rounded-full flex items-center justify-center mx-auto">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">Instant AI Results</h3>
              <p className="text-gray-600 leading-relaxed">
                Get comprehensive disease detection results in seconds using state-of-the-art computer vision technology
              </p>
            </div>
            <div className="space-y-4 p-6 bg-white rounded-xl shadow-lg border border-emerald-100">
              <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-green-600 rounded-full flex items-center justify-center mx-auto">
                <Camera className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">Professional Accuracy</h3>
              <p className="text-gray-600 leading-relaxed">
                Our advanced neural networks are trained on extensive datasets of plant disease images for maximum precision
              </p>
            </div>
            <div className="space-y-4 p-6 bg-white rounded-xl shadow-lg border border-emerald-100">
              <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-green-600 rounded-full flex items-center justify-center mx-auto">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">Expert Treatment Guidance</h3>
              <p className="text-gray-600 leading-relaxed">
                Receive detailed treatment protocols and prevention strategies tailored to specific detected diseases
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Component */}
      <main className="py-8">
        <DiseaseDetectionEnhanced />
      </main>

      <Footer />
    </div>
  );
}
