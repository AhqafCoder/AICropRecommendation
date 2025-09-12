import CropRecommendationForm from "@/components/CropRecommendationForm"

export default function RecommendPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Crop Recommendation</h1>
        <p className="text-gray-600 mt-1">Get AI-powered crop recommendations based on your soil and environmental conditions</p>
      </div>
      <CropRecommendationForm />
    </div>
  )
}