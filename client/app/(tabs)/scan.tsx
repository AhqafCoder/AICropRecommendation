import React, { useState } from 'react';
import { View, Text, StatusBar, Animated, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { 
  Card, 
  Title, 
  Button, 
  Surface,
  Chip,
  Portal,
  Modal
} from 'react-native-paper';
import { 
  Camera, 
  Upload, 
  Scan, 
  Image as ImageIcon,
  Zap,
  Target,
  CheckCircle,
  AlertTriangle,
  Info
} from 'lucide-react-native';

const { width, height } = Dimensions.get('window');

export default function ScanScreen() {
  const [scanMode, setScanMode] = useState<'disease' | 'plant' | 'soil'>('disease');
  const [isScanning, setIsScanning] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const scanOptions = [
    { 
      id: 'disease', 
      title: 'Disease Detection', 
      subtitle: 'Identify plant diseases',
      icon: AlertTriangle, 
      color: '#ef4444',
      bgColor: '#fef2f2' 
    },
    { 
      id: 'plant', 
      title: 'Plant Identification', 
      subtitle: 'Recognize plant species',
      icon: CheckCircle, 
      color: '#22c55e',
      bgColor: '#f0fdf4' 
    },
    { 
      id: 'soil', 
      title: 'Soil Analysis', 
      subtitle: 'Analyze soil conditions',
      icon: Target, 
      color: '#8b5cf6',
      bgColor: '#faf5ff' 
    }
  ];

  const recentScans = [
    { id: 1, type: 'Disease', result: 'Leaf Blight Detected', accuracy: '94%', date: '2 hours ago' },
    { id: 2, type: 'Plant ID', result: 'Tomato Plant', accuracy: '98%', date: '1 day ago' },
    { id: 3, type: 'Soil', result: 'pH: 6.5 - Good', accuracy: '91%', date: '3 days ago' },
  ];

  const handleScan = () => {
    setIsScanning(true);
    // Simulate scanning process
    setTimeout(() => {
      setIsScanning(false);
      setShowResults(true);
    }, 3000);
  };

  return (
    <View className="flex-1 bg-gray-50">
      <StatusBar barStyle="light-content" backgroundColor="#16a34a" />
      
      {/* Header */}
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="pt-12 pb-6 px-5"
      >
        <Text className="text-2xl font-bold text-white mb-2">AI Plant Scanner</Text>
        <Text className="text-white/90">Advanced crop analysis powered by AI</Text>
      </LinearGradient>

      <View className="flex-1 px-4 py-6">
        {/* Scan Mode Selection */}
        <Card className="mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Select Scan Type</Title>
            <View className="space-y-3">
              {scanOptions.map((option) => (
                <Surface
                  key={option.id}
                  className={`rounded-xl p-4 border-2 ${scanMode === option.id ? 'border-green-500' : 'border-gray-200'}`}
                  style={{ backgroundColor: scanMode === option.id ? option.bgColor : '#fff' }}
                  elevation={scanMode === option.id ? 2 : 0}
                >
                  <View className="flex-row items-center">
                    <View 
                      className="rounded-full p-2 mr-4"
                      style={{ backgroundColor: `${option.color}20` }}
                    >
                      <option.icon size={24} color={option.color} />
                    </View>
                    <View className="flex-1">
                      <Text className="text-gray-800 font-semibold text-base">{option.title}</Text>
                      <Text className="text-gray-600 text-sm">{option.subtitle}</Text>
                    </View>
                    {scanMode === option.id && (
                      <CheckCircle size={20} color="#22c55e" />
                    )}
                  </View>
                </Surface>
              ))}
            </View>
          </Card.Content>
        </Card>

        {/* Scanner Interface */}
        <Card className="mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <View className="items-center">
              <View className="relative mb-6">
                <View 
                  className={`w-64 h-64 rounded-3xl border-4 items-center justify-center ${
                    isScanning ? 'border-green-500 bg-green-50' : 'border-dashed border-gray-300 bg-gray-50'
                  }`}
                >
                  {isScanning ? (
                    <View className="items-center">
                      <Animated.View>
                        <Zap size={80} color="#22c55e" />
                      </Animated.View>
                      <Text className="text-green-600 font-semibold mt-4">Scanning...</Text>
                      <Text className="text-gray-600 text-sm">AI Analysis in progress</Text>
                    </View>
                  ) : (
                    <View className="items-center">
                      <Scan size={80} color="#9ca3af" />
                      <Text className="text-gray-600 font-medium mt-4">Position your subject</Text>
                      <Text className="text-gray-500 text-sm text-center px-4">
                        Place the {scanMode} within the frame for analysis
                      </Text>
                    </View>
                  )}
                </View>
                
                {/* Corner guides */}
                {!isScanning && (
                  <>
                    <View className="absolute top-2 left-2 w-6 h-6 border-l-4 border-t-4 border-green-500 rounded-tl-lg" />
                    <View className="absolute top-2 right-2 w-6 h-6 border-r-4 border-t-4 border-green-500 rounded-tr-lg" />
                    <View className="absolute bottom-2 left-2 w-6 h-6 border-l-4 border-b-4 border-green-500 rounded-bl-lg" />
                    <View className="absolute bottom-2 right-2 w-6 h-6 border-r-4 border-b-4 border-green-500 rounded-br-lg" />
                  </>
                )}
              </View>

              <View className="flex-row space-x-4 w-full">
                <Button
                  mode="contained"
                  onPress={handleScan}
                  disabled={isScanning}
                  className="flex-1 bg-green-600"
                  contentStyle={{ paddingVertical: 12 }}
                  labelStyle={{ fontSize: 16, fontWeight: '600' }}
                  icon={() => <Camera size={20} color="#fff" />}
                >
                  {isScanning ? 'Scanning...' : 'Capture'}
                </Button>
                
                <Button
                  mode="outlined"
                  onPress={() => {}}
                  className="flex-1 border-green-600"
                  contentStyle={{ paddingVertical: 12 }}
                  labelStyle={{ color: '#22c55e', fontSize: 16, fontWeight: '600' }}
                  icon={() => <Upload size={20} color="#22c55e" />}
                >
                  Upload
                </Button>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Recent Scans */}
        <Card className="bg-white" elevation={3}>
          <Card.Content className="p-6">
            <View className="flex-row items-center justify-between mb-4">
              <Title className="text-gray-800 font-semibold">Recent Scans</Title>
              <Chip 
                icon={() => <Info size={16} color="#3b82f6" />}
                className="bg-blue-50"
                textStyle={{ color: "#3b82f6", fontSize: 12 }}
              >
                History
              </Chip>
            </View>
            
            {recentScans.map((scan) => (
              <View key={scan.id} className="flex-row items-center py-3 border-b border-gray-100 last:border-b-0">
                <View className="bg-gray-100 rounded-full p-2 mr-4">
                  <ImageIcon size={20} color="#6b7280" />
                </View>
                <View className="flex-1">
                  <Text className="text-gray-800 font-medium">{scan.result}</Text>
                  <View className="flex-row items-center mt-1">
                    <Text className="text-gray-500 text-sm">{scan.type}</Text>
                    <View className="w-1 h-1 bg-gray-400 rounded-full mx-2" />
                    <Text className="text-gray-500 text-sm">{scan.date}</Text>
                  </View>
                </View>
                <Chip 
                  className="bg-green-50"
                  textStyle={{ color: "#22c55e", fontSize: 12 }}
                >
                  {scan.accuracy}
                </Chip>
              </View>
            ))}
          </Card.Content>
        </Card>
      </View>

      {/* Results Modal */}
      <Portal>
        <Modal visible={showResults} onDismiss={() => setShowResults(false)} contentContainerStyle={{ margin: 20 }}>
          <Card className="bg-white">
            <Card.Content className="p-6">
              <View className="items-center mb-6">
                <View className="bg-green-100 rounded-full p-4 mb-4">
                  <CheckCircle size={48} color="#22c55e" />
                </View>
                <Title className="text-gray-800 font-semibold text-center">Scan Complete!</Title>
                <Text className="text-gray-600 text-center">Analysis completed with 94% accuracy</Text>
              </View>
              
              <View className="bg-gray-50 rounded-xl p-4 mb-6">
                <Text className="text-gray-800 font-semibold text-lg mb-2">Results:</Text>
                <Text className="text-gray-700">
                  {scanMode === 'disease' && "No diseases detected. Plant appears healthy."}
                  {scanMode === 'plant' && "Identified: Tomato Plant (Solanum lycopersicum)"}
                  {scanMode === 'soil' && "Soil pH: 6.8 - Optimal for most crops"}
                </Text>
              </View>
              
              <Button
                mode="contained"
                onPress={() => setShowResults(false)}
                className="bg-green-600"
                contentStyle={{ paddingVertical: 8 }}
              >
                View Detailed Report
              </Button>
            </Card.Content>
          </Card>
        </Modal>
      </Portal>
    </View>
  );
}
