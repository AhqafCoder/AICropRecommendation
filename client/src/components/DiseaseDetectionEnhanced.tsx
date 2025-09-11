'use client';

import { useState, useRef, useCallback } from 'react';
import { Upload, Camera, AlertCircle, CheckCircle, Loader2, Eye, RefreshCw, Leaf, Activity, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { diseaseApi, DiseaseDetectionResult } from '@/lib/diseaseApi';
import Image from 'next/image';

const DiseaseDetectionEnhanced = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<DiseaseDetectionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = useCallback((file: File) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setError(null);
      setResult(null);
      
      // Create preview URL
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      
      return () => URL.revokeObjectURL(url);
    } else {
      setError('Please select a valid image file (JPEG, PNG, etc.)');
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  }, [handleFileSelect]);

  const analyzeImage = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setIsAnalyzing(true);
    setError(null);

    try {
      const analysisResult = await diseaseApi.detectDisease(selectedFile, {
        includeExplanation: true
      });
      
      setResult(analysisResult);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Analysis failed. Please try again.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
      setIsAnalyzing(false);
    }
  };

  const reset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'high': return 'destructive';
      case 'medium': return 'secondary';
      case 'low': return 'default';
      default: return 'outline';
    }
  };

  const getConfidenceText = (confidence: number) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50">
      

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

      {/* Upload Section */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader className="bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-t-lg">
          <CardTitle className="flex items-center gap-3 text-xl">
            <div className="p-2 bg-white/20 rounded-full">
              <Camera className="h-6 w-6" />
            </div>
            Professional Image Upload
          </CardTitle>
          <CardDescription className="text-emerald-100">
            Upload clear, high-resolution images of affected crop areas for accurate AI analysis
          </CardDescription>
        </CardHeader>
        <CardContent className="p-8">
          {!selectedFile ? (
            <div
              className="border-2 border-dashed border-emerald-300 bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl p-12 text-center hover:border-emerald-400 hover:bg-gradient-to-br hover:from-emerald-100 hover:to-green-100 transition-all duration-300 cursor-pointer group"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="group-hover:scale-105 transition-transform duration-300">
                <Upload className="h-16 w-16 mx-auto mb-6 text-emerald-500" />
                <div className="space-y-3">
                  <p className="text-xl font-semibold text-gray-800">Drop your crop image here or click to browse</p>
                  <p className="text-sm text-gray-600">
                    Supports JPEG, PNG, WebP • Maximum size: 10MB • Recommended: High resolution leaf/plant images
                  </p>
                  <div className="flex items-center justify-center gap-4 mt-6">
                    <Badge variant="outline" className="bg-white border-emerald-200 text-emerald-700">
                      <Leaf className="h-3 w-3 mr-1" />
                      Crop Diseases
                    </Badge>
                    <Badge variant="outline" className="bg-white border-emerald-200 text-emerald-700">
                      <Activity className="h-3 w-3 mr-1" />
                      Real-time Analysis
                    </Badge>
                  </div>
                </div>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileInputChange}
                className="hidden"
              />
            </div>
          ) : (
            <div className="space-y-6">
              <div className="relative rounded-xl overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100 border border-gray-200 h-80">
                {previewUrl && (
                  <Image
                    src={previewUrl}
                    alt="Selected crop image"
                    fill
                    className="object-contain"
                  />
                )}
              </div>
              <div className="flex items-center justify-between bg-gradient-to-r from-emerald-50 to-green-50 p-4 rounded-lg border border-emerald-200">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-emerald-500 rounded-full">
                    <CheckCircle className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <span className="font-semibold text-gray-800">{selectedFile.name}</span>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge variant="outline" className="bg-white border-emerald-300 text-emerald-700">
                        {(selectedFile.size / 1024 / 1024).toFixed(1)} MB
                      </Badge>
                      <Badge variant="outline" className="bg-white border-emerald-300 text-emerald-700">
                        Ready for Analysis
                      </Badge>
                    </div>
                  </div>
                </div>
                <div className="flex gap-3">
                  <Button variant="outline" size="sm" onClick={reset} className="border-emerald-300 text-emerald-700 hover:bg-emerald-50">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Change Image
                  </Button>
                  <Button 
                    onClick={analyzeImage}
                    disabled={isLoading}
                    className="bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white min-w-40 shadow-lg"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Eye className="h-4 w-4 mr-2" />
                        Analyze Image
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Loading State */}
      {isAnalyzing && (
        <Card className="shadow-lg border-0 bg-white/90 backdrop-blur-sm">
          <CardContent className="pt-8 pb-8">
            <div className="space-y-6">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-gradient-to-r from-emerald-500 to-green-600 rounded-full">
                  <Loader2 className="h-6 w-6 animate-spin text-white" />
                </div>
                <div>
                  <span className="text-xl font-semibold text-gray-800">AI Analysis in Progress</span>
                  <p className="text-gray-600">Our advanced neural network is examining your crop image...</p>
                </div>
              </div>
              <div className="space-y-3">
                <Progress value={75} className="w-full h-3 bg-gray-200" />
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Processing image quality...</span>
                  <span>75% complete</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-8">
          {/* Main Results Card */}
          <Card className="shadow-xl border-0 bg-white/90 backdrop-blur-sm overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-emerald-500 to-green-600 text-white">
              <CardTitle className="flex items-center justify-between text-2xl">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-white/20 rounded-full">
                    <Activity className="h-6 w-6" />
                  </div>
                  <span>AI Detection Results</span>
                </div>
                <Badge 
                  variant={getRiskColor(result.risk_assessment.overall_risk)}
                  className="text-sm px-3 py-1 bg-white/20 border-white/30"
                >
                  {result.risk_assessment.overall_risk} Risk Level
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="p-8 space-y-8">
              {/* Disease Information */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="bg-gradient-to-br from-emerald-50 to-green-50 p-6 rounded-xl border border-emerald-200">
                    <h3 className="font-bold text-2xl mb-3 text-gray-800 flex items-center gap-2">
                      <Leaf className="h-6 w-6 text-emerald-600" />
                      Disease Identified
                    </h3>
                    <p className="text-3xl font-bold text-emerald-700 mb-2">{result.predicted_class}</p>
                    <p className="text-gray-600 font-medium">Affected Crop: <span className="text-emerald-600">{result.crop}</span></p>
                  </div>
                  
                  <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                    <h4 className="font-bold text-lg mb-4 text-gray-800 flex items-center gap-2">
                      <Activity className="h-5 w-5 text-emerald-600" />
                      Confidence Analysis
                    </h4>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span className="font-medium text-gray-700">{getConfidenceText(result.confidence)}</span>
                        <span className="text-xl font-bold text-emerald-600">{(result.confidence * 100).toFixed(1)}%</span>
                      </div>
                      <Progress 
                        value={result.confidence * 100} 
                        className="w-full h-4"
                      />
                      <p className="text-sm text-gray-500">Based on advanced neural network analysis</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-6">
                  {result.disease_info.description && (
                    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-full">
                      <h4 className="font-bold text-lg mb-4 text-gray-800 flex items-center gap-2">
                        <AlertCircle className="h-5 w-5 text-emerald-600" />
                        Disease Description
                      </h4>
                      <p className="text-gray-700 leading-relaxed">
                        {result.disease_info.description}
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Visual Explanation */}
              {result.explanation?.explanation_image && (
                <div className="bg-gradient-to-br from-emerald-50 to-green-50 p-6 rounded-xl border border-emerald-200">
                  <div className="flex items-center justify-between mb-6">
                    <h4 className="font-bold text-lg text-gray-800 flex items-center gap-2">
                      <Eye className="h-5 w-5 text-emerald-600" />
                      AI Visual Analysis (Grad-CAM)
                    </h4>
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button variant="outline" size="sm" className="border-emerald-300 text-emerald-700 hover:bg-emerald-100">
                          <Eye className="h-4 w-4 mr-2" />
                          View Detailed Analysis
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-5xl">
                        <DialogHeader>
                          <DialogTitle className="text-xl flex items-center gap-2">
                            <Activity className="h-5 w-5 text-emerald-600" />
                            Comprehensive Visual Analysis
                          </DialogTitle>
                          <DialogDescription>
                            Grad-CAM heatmap visualization showing critical areas the AI neural network focused on during disease detection
                          </DialogDescription>
                        </DialogHeader>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                          <div className="space-y-3">
                            <h5 className="font-semibold text-gray-800">Original Crop Image</h5>
                            {previewUrl && (
                              <div className="relative w-full h-64 rounded-lg border-2 border-gray-200 shadow-sm overflow-hidden">
                                <Image
                                  src={previewUrl}
                                  alt="Original crop image"
                                  fill
                                  className="object-contain"
                                />
                              </div>
                            )}
                          </div>
                          <div className="space-y-3">
                            <h5 className="font-semibold text-gray-800">AI Focus Areas (Grad-CAM Heatmap)</h5>
                            <div className="relative w-full h-64 rounded-lg border-2 border-emerald-200 shadow-sm overflow-hidden">
                              <Image
                                src={`data:image/png;base64,${result.explanation.explanation_image}`}
                                alt="Grad-CAM heatmap overlay"
                                fill
                                className="object-contain"
                              />
                            </div>
                            <p className="text-sm text-gray-600 bg-emerald-50 p-3 rounded">
                              <strong>Red/Yellow regions:</strong> Areas where the AI detected disease indicators with high confidence
                            </p>
                          </div>
                        </div>
                      </DialogContent>
                    </Dialog>
                  </div>
                  <div className="relative rounded-lg overflow-hidden border-2 border-emerald-200 shadow-sm h-64 bg-white">
                    <Image
                      src={`data:image/png;base64,${result.explanation.explanation_image}`}
                      alt="AI analysis visualization"
                      fill
                      className="object-contain"
                    />
                  </div>
                  <p className="text-sm text-gray-600 mt-3 bg-white p-3 rounded-lg">
                    <strong>AI Explanation:</strong> Highlighted areas show regions where disease symptoms were detected with highest confidence
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Detailed Information Cards - All visible simultaneously */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recommendations Card */}
            <Card className="shadow-lg border-0 bg-gradient-to-br from-emerald-50 to-green-50 border-emerald-200">
              <CardHeader className="bg-gradient-to-r from-emerald-500 to-green-600 text-white">
                <CardTitle className="flex items-center gap-3 text-lg">
                  <div className="p-2 bg-white/20 rounded-full">
                    <CheckCircle className="h-5 w-5" />
                  </div>
                  Treatment Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                {result.risk_assessment.recommendations.length > 0 ? (
                  <ul className="space-y-4">
                    {result.risk_assessment.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm border border-emerald-100">
                        <div className="bg-emerald-500 rounded-full p-1.5 mt-0.5 flex-shrink-0">
                          <CheckCircle className="h-3 w-3 text-white" />
                        </div>
                        <span className="text-sm leading-relaxed text-gray-700 font-medium">{rec}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-600 bg-white p-4 rounded-lg">No specific recommendations available for this condition.</p>
                )}
              </CardContent>
            </Card>

            {/* Symptoms Card */}
            <Card className="shadow-lg border-0 bg-gradient-to-br from-orange-50 to-amber-50 border-orange-200">
              <CardHeader className="bg-gradient-to-r from-orange-500 to-amber-600 text-white">
                <CardTitle className="flex items-center gap-3 text-lg">
                  <div className="p-2 bg-white/20 rounded-full">
                    <AlertCircle className="h-5 w-5" />
                  </div>
                  Disease Symptoms
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                {result.disease_info.symptoms && result.disease_info.symptoms.length > 0 ? (
                  <ul className="space-y-4">
                    {result.disease_info.symptoms.map((symptom, index) => (
                      <li key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm border border-orange-100">
                        <div className="bg-orange-500 rounded-full p-1.5 mt-0.5 flex-shrink-0">
                          <AlertCircle className="h-3 w-3 text-white" />
                        </div>
                        <span className="text-sm leading-relaxed text-gray-700 font-medium">{symptom}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-600 bg-white p-4 rounded-lg">No symptoms information available for this disease.</p>
                )}
              </CardContent>
            </Card>

            {/* Prevention Card */}
            <Card className="shadow-lg border-0 bg-gradient-to-br from-emerald-50 to-teal-50 border-teal-200">
              <CardHeader className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white">
                <CardTitle className="flex items-center gap-3 text-lg">
                  <div className="p-2 bg-white/20 rounded-full">
                    <Shield className="h-5 w-5" />
                  </div>
                  Prevention Measures
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                {result.disease_info.prevention && result.disease_info.prevention.length > 0 ? (
                  <ul className="space-y-4">
                    {result.disease_info.prevention.map((prev, index) => (
                      <li key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm border border-teal-100">
                        <div className="bg-teal-500 rounded-full p-1.5 mt-0.5 flex-shrink-0">
                          <Shield className="h-3 w-3 text-white" />
                        </div>
                        <span className="text-sm leading-relaxed text-gray-700 font-medium">{prev}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-600 bg-white p-4 rounded-lg">No prevention information available for this disease.</p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      )}
      </div>
    </div>
  );
};

export default DiseaseDetectionEnhanced;