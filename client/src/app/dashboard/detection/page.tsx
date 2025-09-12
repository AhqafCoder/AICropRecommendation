import DiseaseDetection from "@/components/DiseaseDetection"

export default function DetectionPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Disease Detection</h1>
        <p className="text-gray-600 mt-1">Upload images of your crops to detect diseases using AI</p>
      </div>
      <DiseaseDetection />
    </div>
  )
}