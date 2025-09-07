import React, { useState } from 'react';
import { View, Text, ScrollView, StatusBar, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { 
  Card, 
  Title, 
  Chip, 
  Surface,
  SegmentedButtons,
  ProgressBar
} from 'react-native-paper';
import { 
  BarChart3, 
  TrendingUp, 
  Activity, 
  Droplets,
  Thermometer,
  Sun,
  Target,
  AlertCircle,
  CheckCircle,
  Calendar,
  Leaf
} from 'lucide-react-native';

const { width } = Dimensions.get('window');

export default function AnalysisScreen() {
  const [selectedPeriod, setSelectedPeriod] = useState('week');

  const cropMetrics = [
    { 
      label: "Overall Health", 
      value: 87, 
      unit: "%", 
      icon: Activity, 
      color: "#22c55e",
      status: "excellent",
      change: "+5%"
    },
    { 
      label: "Growth Rate", 
      value: 92, 
      unit: "%", 
      icon: TrendingUp, 
      color: "#3b82f6",
      status: "good",
      change: "+12%"
    },
    { 
      label: "Water Efficiency", 
      value: 78, 
      unit: "%", 
      icon: Droplets, 
      color: "#06b6d4",
      status: "good",
      change: "-2%"
    },
    { 
      label: "Soil Quality", 
      value: 85, 
      unit: "%", 
      icon: Target, 
      color: "#8b5cf6",
      status: "excellent",
      change: "+8%"
    }
  ];

  const environmentalData = [
    { label: "Temperature", value: "24°C", optimal: "22-26°C", status: "optimal", icon: Thermometer },
    { label: "Humidity", value: "68%", optimal: "60-70%", status: "optimal", icon: Droplets },
    { label: "Light Exposure", value: "8.5h", optimal: "8-10h", status: "optimal", icon: Sun },
    { label: "Soil pH", value: "6.8", optimal: "6.0-7.0", status: "optimal", icon: Leaf }
  ];

  const yieldPrediction = {
    current: 2.8,
    predicted: 3.2,
    lastSeason: 2.5,
    improvement: "+28%"
  };

  const alerts = [
    { type: "warning", message: "Water levels slightly below optimal", icon: AlertCircle, color: "#f59e0b" },
    { type: "success", message: "Growth rate exceeding expectations", icon: CheckCircle, color: "#22c55e" },
    { type: "info", message: "Harvest window: 35-45 days", icon: Calendar, color: "#3b82f6" }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return '#22c55e';
      case 'good': return '#3b82f6';
      case 'warning': return '#f59e0b';
      case 'poor': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <View className="flex-1 bg-gray-50">
      <StatusBar barStyle="light-content" backgroundColor="#16a34a" />
      
      {/* Header */}
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="pt-12 pb-6 px-5"
      >
        <Text className="text-2xl font-bold text-white mb-2">Crop Analytics</Text>
        <Text className="text-white/90">Comprehensive performance analysis</Text>
      </LinearGradient>

      <ScrollView 
        className="flex-1" 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        {/* Time Period Selector */}
        <View className="px-4 py-4">
          <SegmentedButtons
            value={selectedPeriod}
            onValueChange={setSelectedPeriod}
            buttons={[
              { value: 'week', label: 'Week' },
              { value: 'month', label: 'Month' },
              { value: 'season', label: 'Season' }
            ]}
            style={{ backgroundColor: '#fff' }}
          />
        </View>

        {/* Yield Prediction Card */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <View className="flex-row items-center justify-between mb-4">
              <Title className="text-gray-800 font-semibold">Yield Prediction</Title>
              <Chip 
                icon={() => <TrendingUp size={16} color="#22c55e" />}
                className="bg-green-50"
                textStyle={{ color: "#22c55e", fontSize: 12 }}
              >
                {yieldPrediction.improvement}
              </Chip>
            </View>
            
            <View className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-4">
              <View className="flex-row justify-between items-center mb-3">
                <View>
                  <Text className="text-gray-600 text-sm">Predicted Yield</Text>
                  <Text className="text-3xl font-bold text-gray-800">{yieldPrediction.predicted} tons</Text>
                </View>
                <View className="items-end">
                  <Text className="text-gray-600 text-sm">Last Season</Text>
                  <Text className="text-xl font-semibold text-gray-700">{yieldPrediction.lastSeason} tons</Text>
                </View>
              </View>
              
              <View className="mt-2">
                <Text className="text-gray-600 text-sm mb-1">Progress to Target</Text>
                <ProgressBar 
                  progress={yieldPrediction.current / yieldPrediction.predicted} 
                  color="#22c55e"
                  style={{ height: 8, borderRadius: 4, backgroundColor: '#e5e7eb' }}
                />
                <Text className="text-gray-500 text-xs mt-1">
                  {yieldPrediction.current} / {yieldPrediction.predicted} tons
                </Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Key Metrics */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Performance Metrics</Title>
            <View className="space-y-4">
              {cropMetrics.map((metric, index) => (
                <View key={index} className="bg-gray-50 rounded-xl p-4">
                  <View className="flex-row items-center justify-between mb-3">
                    <View className="flex-row items-center">
                      <View 
                        className="rounded-full p-2 mr-3"
                        style={{ backgroundColor: `${metric.color}20` }}
                      >
                        <metric.icon size={20} color={metric.color} />
                      </View>
                      <Text className="text-gray-800 font-medium">{metric.label}</Text>
                    </View>
                    <View className="items-end">
                      <Text className="text-2xl font-bold text-gray-800">
                        {metric.value}{metric.unit}
                      </Text>
                      <Text 
                        className="text-sm font-medium"
                        style={{ color: metric.change.startsWith('+') ? '#22c55e' : '#ef4444' }}
                      >
                        {metric.change}
                      </Text>
                    </View>
                  </View>
                  <ProgressBar 
                    progress={metric.value / 100} 
                    color={metric.color}
                    style={{ height: 6, borderRadius: 3, backgroundColor: '#e5e7eb' }}
                  />
                </View>
              ))}
            </View>
          </Card.Content>
        </Card>

        {/* Environmental Conditions */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Environmental Conditions</Title>
            <View className="grid grid-cols-2 gap-3">
              {environmentalData.map((env, index) => (
                <Surface key={index} className="bg-gray-50 rounded-xl p-4" elevation={1}>
                  <View className="items-center">
                    <View className="bg-white rounded-full p-2 mb-2">
                      <env.icon size={24} color="#22c55e" />
                    </View>
                    <Text className="text-lg font-bold text-gray-800">{env.value}</Text>
                    <Text className="text-gray-600 text-sm text-center">{env.label}</Text>
                    <Text className="text-green-600 text-xs mt-1">Optimal: {env.optimal}</Text>
                  </View>
                </Surface>
              ))}
            </View>
          </Card.Content>
        </Card>

        {/* Alerts & Recommendations */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Alerts & Insights</Title>
            <View className="space-y-3">
              {alerts.map((alert, index) => (
                <View 
                  key={index} 
                  className="flex-row items-center p-3 rounded-xl"
                  style={{ backgroundColor: `${alert.color}10` }}
                >
                  <View 
                    className="rounded-full p-2 mr-3"
                    style={{ backgroundColor: `${alert.color}20` }}
                  >
                    <alert.icon size={16} color={alert.color} />
                  </View>
                  <Text className="flex-1 text-gray-800">{alert.message}</Text>
                </View>
              ))}
            </View>
          </Card.Content>
        </Card>

        {/* Growth Chart Placeholder */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <View className="flex-row items-center justify-between mb-4">
              <Title className="text-gray-800 font-semibold">Growth Trends</Title>
              <BarChart3 size={24} color="#22c55e" />
            </View>
            
            <View className="bg-gray-50 rounded-xl p-8 items-center">
              <BarChart3 size={48} color="#9ca3af" />
              <Text className="text-gray-600 font-medium mt-4">Interactive Chart</Text>
              <Text className="text-gray-500 text-sm text-center">
                Detailed growth analytics and historical trends would be displayed here
              </Text>
            </View>
          </Card.Content>
        </Card>
      </ScrollView>
    </View>
  );
}
