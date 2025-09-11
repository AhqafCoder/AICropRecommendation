"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Upload, Camera, AlertTriangle, CheckCircle, Loader2, Wifi, WifiOff, Info } from "lucide-react";
import { diseaseApi, DiseaseDetectionResult, formatDiseaseName, getSeverityColor, getRiskIcon } from "@/lib/diseaseApi";

export default function DiseaseDetection() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [result, setResult] = useState<DiseaseDetectionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [error, setError] = useState<string | null>(null);

  // Create a ref for the file input
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    setApiStatus('checking');
    try {
      const isOnline = await diseaseApi.healthCheck();
      setApiStatus(isOnline ? 'online' : 'offline');
    } catch (error) {
      console.error('API status check failed:', error);
      setApiStatus('offline');
    }
  };

  const triggerFileSelect = () => {
    console.log('Triggering file select...');
    fileInputRef.current?.click();
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    
    console.log('File selected:', file);
    
    if (file) {
      // Reset previous states
      setError(null);
      setResult(null);
      
      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'];
      if (!allowedTypes.includes(file.type)) {
        setError('Please select a valid image file (JPEG, PNG, BMP, or TIFF)');
        return;
      }
      
      // Validate file size (10MB limit)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        setError('Image size must be less than 10MB');
        return;
      }
      
      console.log('File validation passed, setting image...');
      setSelectedImage(file);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        console.log('Image loaded for preview');
        setImagePreview(e.target?.result as string);
      };
      reader.onerror = (e) => {
        console.error('Error reading file:', e);
        setError('Error reading the image file');
      };
      reader.readAsDataURL(file);
    } else {
      console.log('No file selected');
    }
    
    // Clear the input value to allow selecting the same file again
    e.target.value = '';
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;
    
    if (apiStatus === 'offline') {
      setError('Disease detection service is currently unavailable. Please try again later.');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const detectionResult = await diseaseApi.detectDisease(selectedImage, {
        includeExplanation: true,
        // You can add weather data here if available
        // weatherHumidity: 70,
        // weatherTemperature: 25,
        // weatherRainfall: 100
      });
      
      setResult(detectionResult);
    } catch (error) {
      console.error('Disease detection failed:', error);
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('An unexpected error occurred during disease detection');
      }
    } finally {
      setLoading(false);
    }
  };

  const getLocalSeverityColor = (risk: string) => {
    return getSeverityColor(risk);
  };

  const getSeverityIcon = (risk: string) => {
    switch (risk.toLowerCase()) {
      case "high": return <AlertTriangle className="w-4 h-4" />;
      case "medium": return <AlertTriangle className="w-4 h-4" />;
      case "low": return <CheckCircle className="w-4 h-4" />;
      default: return <CheckCircle className="w-4 h-4" />;
    }
  };

  const getApiStatusIcon = () => {
    switch (apiStatus) {
      case 'online': return <Wifi className="w-4 h-4 text-green-600" />;
      case 'offline': return <WifiOff className="w-4 h-4 text-red-600" />;
      case 'checking': return <Loader2 className="w-4 h-4 animate-spin text-gray-600" />;
    }
  };

  const getApiStatusText = () => {
    switch (apiStatus) {
      case 'online': return 'AI Service Online';
      case 'offline': return 'AI Service Offline';
      case 'checking': return 'Checking...';
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
              <div className="ml-auto flex items-center gap-2 text-sm">
                {getApiStatusIcon()}
                <span className={`${apiStatus === 'online' ? 'text-green-600' : apiStatus === 'offline' ? 'text-red-600' : 'text-gray-600'}`}>
                  {getApiStatusText()}
                </span>
              </div>
            </CardTitle>
            <CardDescription>
              Upload a clear image of your plant leaves to detect diseases instantly using AI
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Image Upload */}
            <div 
              className="relative border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-green-500 transition-colors cursor-pointer bg-gray-50 hover:bg-gray-100"
              onClick={triggerFileSelect}
            >
              {imagePreview ? (
                <div className="space-y-4">
                  <Image
                    src={imagePreview}
                    alt="Selected plant"
                    width={192}
                    height={192}
                    className="max-w-full h-48 object-cover rounded-lg mx-auto border"
                  />
                  <div className="flex gap-2 justify-center">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        triggerFileSelect();
                      }}
                    >
                      <Upload className="w-4 h-4 mr-1" />
                      Change Image
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedImage(null);
                        setImagePreview(null);
                        setResult(null);
                        setError(null);
                      }}
                    >
                      Remove
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4 pointer-events-none">
                  <Upload className="w-12 h-12 text-gray-400 mx-auto" />
                  <div>
                    <p className="text-gray-600 font-medium">Click to upload or drag and drop</p>
                    <p className="text-sm text-gray-500 mt-1">PNG, JPG, BMP, TIFF up to 10MB</p>
                    <Button
                      variant="outline"
                      size="sm"
                      className="mt-3 pointer-events-auto"
                      onClick={(e) => {
                        e.stopPropagation();
                        triggerFileSelect();
                      }}
                    >
                      <Upload className="w-4 h-4 mr-1" />
                      Select Image
                    </Button>
                  </div>
                </div>
              )}
              
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/jpg,image/png,image/bmp,image/tiff"
                onChange={handleImageSelect}
                className="hidden"
                disabled={loading}
              />
            </div>

            {/* Analyze Button */}
            {selectedImage && (
              <Button
                onClick={handleAnalyze}
                disabled={loading || apiStatus === 'offline'}
                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Analyzing Image...
                  </>
                ) : apiStatus === 'offline' ? (
                  <>
                    <WifiOff className="w-4 h-4 mr-2" />
                    Service Unavailable
                  </>
                ) : (
                  <>
                    <Camera className="w-4 h-4 mr-2" />
                    Detect Disease
                  </>
                )}
              </Button>
            )}

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h4 className="font-medium text-red-900 mb-1">
                      {error.includes('Image size') || error.includes('image file') ? 'Upload Error' : 'Detection Failed'}
                    </h4>
                    <p className="text-sm text-red-800">{error}</p>
                    <div className="mt-2 flex gap-2">
                      {apiStatus === 'offline' && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={checkApiStatus}
                          className="border-red-200 text-red-700 hover:bg-red-50"
                        >
                          <Loader2 className={`w-3 h-3 mr-1 ${apiStatus === 'checking' ? 'animate-spin' : ''}`} />
                          Retry Connection
                        </Button>
                      )}
                      {(error.includes('Image size') || error.includes('image file')) && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setError(null);
                            setSelectedImage(null);
                            setImagePreview(null);
                          }}
                          className="border-red-200 text-red-700 hover:bg-red-50"
                        >
                          Try Another Image
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
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

            {/* Debug Info */}
            {process.env.NODE_ENV === 'development' && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                <h4 className="font-medium text-gray-900 mb-2 text-sm">Debug Info:</h4>
                <ul className="text-xs text-gray-600 space-y-1">
                  <li>• API Status: {apiStatus}</li>
                  <li>• Selected Image: {selectedImage ? selectedImage.name : 'None'}</li>
                  <li>• Image Size: {selectedImage ? `${(selectedImage.size / 1024 / 1024).toFixed(2)} MB` : 'N/A'}</li>
                  <li>• API URL: {process.env.NEXT_PUBLIC_DISEASE_API_URL || 'http://localhost:8001'}</li>
                </ul>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={checkApiStatus}
                  className="mt-2"
                >
                  Test API Connection
                </Button>
              </div>
            )}
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
                    <Badge className={getLocalSeverityColor(result.risk_assessment.overall_risk)}>
                      {getSeverityIcon(result.risk_assessment.overall_risk)}
                      <span className="ml-1">{result.risk_assessment.overall_risk} Risk</span>
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-gray-900">
                        {formatDiseaseName(result.predicted_class)}
                      </div>
                      <div className="text-sm text-gray-600">
                        {Math.round(result.confidence * 100)}% Confidence
                      </div>
                      {result.crop && result.crop !== 'Unknown' && (
                        <div className="text-sm text-blue-600 mt-1">
                          Crop: {result.crop}
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Treatment Recommendations */}
              {result.disease_info.solutions && result.disease_info.solutions.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Treatment Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.disease_info.solutions.map((treatment: string, index: number) => (
                        <li key={index} className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-gray-700">{treatment}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Preventive Measures */}
              {result.disease_info.prevention && result.disease_info.prevention.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Preventive Measures</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.disease_info.prevention.map((measure: string, index: number) => (
                        <li key={index} className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-gray-700">{measure}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Symptoms */}
              {result.disease_info.symptoms && result.disease_info.symptoms.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Symptoms</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.disease_info.symptoms.map((symptom: string, index: number) => (
                        <li key={index} className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-orange-600 rounded-full mt-2 flex-shrink-0"></div>
                          <span className="text-gray-700">{symptom}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}

              {/* Risk Assessment Details */}
              {result.risk_assessment.risk_factors && result.risk_assessment.risk_factors.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Risk Assessment</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div>
                        <h4 className="font-medium mb-2">Risk Factors:</h4>
                        <ul className="space-y-1">
                          {result.risk_assessment.risk_factors.map((factor: string, index: number) => (
                            <li key={index} className="flex items-start gap-2 text-sm">
                              <div className="w-1.5 h-1.5 bg-red-500 rounded-full mt-1.5 flex-shrink-0"></div>
                              <span className="text-gray-600">{factor}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      {result.risk_assessment.recommendations && result.risk_assessment.recommendations.length > 0 && (
                        <div>
                          <h4 className="font-medium mb-2">Recommendations:</h4>
                          <ul className="space-y-1">
                            {result.risk_assessment.recommendations.map((rec: string, index: number) => (
                              <li key={index} className="flex items-start gap-2 text-sm">
                                <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1.5 flex-shrink-0"></div>
                                <span className="text-gray-600">{rec}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Top Predictions */}
              {result.class_probabilities && Object.keys(result.class_probabilities).length > 1 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Alternative Predictions</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {Object.entries(result.class_probabilities)
                        .sort(([,a], [,b]) => b - a)
                        .slice(0, 3)
                        .map(([className, probability], index) => (
                          <div key={index} className="flex items-center justify-between">
                            <span className="text-sm text-gray-700">
                              {formatDiseaseName(className)}
                            </span>
                            <span className="text-sm font-medium">
                              {Math.round(probability * 100)}%
                            </span>
                          </div>
                        ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Disclaimer */}
              <Card className="bg-yellow-50 border-yellow-200">
                <CardContent className="pt-6">
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                    <div className="text-sm text-yellow-800">
                      <strong>Disclaimer:</strong> This is an AI-based preliminary diagnosis. 
                      For severe cases or uncertain results, please consult with a local 
                      agricultural expert or extension officer. The AI model is trained on 
                      specific crop diseases and may not cover all possible conditions.
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {!result && !loading && !error && (
            <Card>
              <CardContent className="text-center py-8">
                <Camera className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">
                  Upload an image to get instant disease detection results
                </p>
                {apiStatus === 'offline' && (
                  <p className="text-red-500 text-sm mt-2">
                    AI service is currently unavailable
                  </p>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
