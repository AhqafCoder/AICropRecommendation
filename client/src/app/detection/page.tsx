import Header from "@/components/Header";
import Footer from "@/components/Footer";
import DiseaseDetection from "@/components/DiseaseDetection";
import { Camera, Zap, Shield } from "lucide-react";

export default function DiseaseDetectionPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Page Header */}
      <section className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/20 text-white text-sm font-medium mb-6">
              <Camera className="w-4 h-4 mr-2" />
              AI Image Recognition
            </div>
            <h1 className="text-4xl sm:text-5xl font-bold mb-4">
              Real-Time Plant Disease Detection
            </h1>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              Upload a photo of your crop and get instant AI-powered disease diagnosis 
              with treatment recommendations.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="space-y-3">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                <Zap className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Instant Results</h3>
              <p className="text-gray-600">
                Get disease detection results in seconds using advanced computer vision
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                <Camera className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">High Accuracy</h3>
              <p className="text-gray-600">
                Our AI models are trained on thousands of plant disease images
              </p>
            </div>
            <div className="space-y-3">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                <Shield className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Treatment Guidance</h3>
              <p className="text-gray-600">
                Get specific treatment and prevention recommendations for detected diseases
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Component */}
      <main className="py-8">
        <DiseaseDetection />
      </main>

      <Footer />
    </div>
  );
}
