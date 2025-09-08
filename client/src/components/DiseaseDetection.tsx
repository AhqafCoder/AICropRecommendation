"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Upload, Camera, AlertTriangle, CheckCircle, Loader2 } from "lucide-react";

interface DiseaseDetectionResult {
  disease: string;
  confidence: number;
  severity: "Low" | "Medium" | "High";
  treatment: string[];
  preventive_measures: string[];
}

export default function DiseaseDetection() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [result, setResult] = useState<DiseaseDetectionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    
    // Simulate AI analysis for demo
    setTimeout(() => {
      // Mock disease detection result
      const mockResults: DiseaseDetectionResult[] = [
        {
          disease: "Leaf Blight",
          confidence: 0.92,
          severity: "Medium",
          treatment: [
            "Apply copper-based fungicide",
            "Remove affected leaves",
            "Improve air circulation"
          ],
          preventive_measures: [
            "Avoid overhead watering",
            "Plant resistant varieties",
            "Maintain proper spacing"
          ]
        },
        {
          disease: "Powdery Mildew",
          confidence: 0.87,
          severity: "Low",
          treatment: [
            "Apply sulfur-based fungicide",
            "Increase sunlight exposure",
            "Reduce humidity around plants"
          ],
          preventive_measures: [
            "Ensure good air circulation",
            "Avoid overcrowding",
            "Water at soil level"
          ]
        },
        {
          disease: "Healthy Plant",
          confidence: 0.95,
          severity: "Low",
          treatment: [
            "Continue current care routine",
            "Monitor regularly",
            "Maintain optimal conditions"
          ],
          preventive_measures: [
            "Regular watering schedule",
            "Balanced fertilization",
            "Regular inspection"
          ]
        }
      ];

      const randomResult = mockResults[Math.floor(Math.random() * mockResults.length)];
      setResult(randomResult);
      setLoading(false);
    }, 2000);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "High": return "bg-red-100 text-red-800";
      case "Medium": return "bg-yellow-100 text-yellow-800";
      case "Low": return "bg-green-100 text-green-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "High": return <AlertTriangle className="w-4 h-4" />;
      case "Medium": return <AlertTriangle className="w-4 h-4" />;
      case "Low": return <CheckCircle className="w-4 h-4" />;
      default: return <CheckCircle className="w-4 h-4" />;
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Camera className="w-5 h-5 text-green-600" />
              Plant Disease Detection
            </CardTitle>
            <CardDescription>
              Upload a clear image of your plant leaves to detect diseases instantly
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Image Upload */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-green-500 transition-colors">
              {imagePreview ? (
                <div className="space-y-4">
                  <img
                    src={imagePreview}
                    alt="Selected plant"
                    className="max-w-full h-48 object-cover rounded-lg mx-auto"
                  />
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSelectedImage(null);
                      setImagePreview(null);
                      setResult(null);
                    }}
                  >
                    Change Image
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <Upload className="w-12 h-12 text-gray-400 mx-auto" />
                  <div>
                    <p className="text-gray-600">Click to upload or drag and drop</p>
                    <p className="text-sm text-gray-500">PNG, JPG up to 10MB</p>
                  </div>
                </div>
              )}
              
              <input
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
            </div>

            {/* Analyze Button */}
            {selectedImage && (
              <Button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full bg-green-600 hover:bg-green-700"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Analyzing Image...
                  </>
                ) : (
                  <>
                    <Camera className="w-4 h-4 mr-2" />
                    Detect Disease
                  </>
                )}
              </Button>
            )}

            {/* Tips */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-2">For Best Results:</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Take photos in good lighting</li>
                <li>• Focus on affected leaves</li>
                <li>• Include multiple symptoms if visible</li>
                <li>• Avoid blurry or dark images</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        <div className="space-y-6">
          {result && (
            <>
              {/* Detection Result */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    Detection Result
                    <Badge className={getSeverityColor(result.severity)}>
                      {getSeverityIcon(result.severity)}
                      <span className="ml-1">{result.severity} Risk</span>
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">
                        {result.disease}
                      </div>
                      <div className="text-sm text-gray-600">
                        {Math.round(result.confidence * 100)}% Confidence
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Treatment Recommendations */}
              <Card>
                <CardHeader>
                  <CardTitle>Treatment Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {result.treatment.map((treatment, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{treatment}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Preventive Measures */}
              <Card>
                <CardHeader>
                  <CardTitle>Preventive Measures</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {result.preventive_measures.map((measure, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-gray-700">{measure}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* Disclaimer */}
              <Card className="bg-yellow-50 border-yellow-200">
                <CardContent className="pt-6">
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                    <div className="text-sm text-yellow-800">
                      <strong>Disclaimer:</strong> This is an AI-based preliminary diagnosis. 
                      For severe cases or uncertain results, please consult with a local 
                      agricultural expert or extension officer.
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {!result && !loading && (
            <Card>
              <CardContent className="text-center py-8">
                <Camera className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">
                  Upload an image to get instant disease detection results
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
