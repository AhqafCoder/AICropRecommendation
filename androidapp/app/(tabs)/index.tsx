import React, { useState } from 'react';
import { 
  View, 
  Text, 
  ScrollView, 
  TouchableOpacity, 
  Dimensions,
  StatusBar,
  ImageBackground
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { 
  Card, 
  Title, 
  Paragraph, 
  Button, 
  Chip,
  Surface,
  Avatar,
  IconButton
} from 'react-native-paper';
import { 
  MapPin, 
  Cloud, 
  Droplets, 
  Wind, 
  TrendingUp,
  Activity,
  Leaf,
  Sun,
  Eye,
  Bell,
  Settings,
  ThermometerSun
} from 'lucide-react-native';

const { width } = Dimensions.get('window');

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const [currentWeather] = useState({
    location: "Farm Location: North Valley",
    temperature: "24°C",
    condition: "Partly Cloudy",
    humidity: "68%",
    wind: "12 km/h",
    uvIndex: "Moderate"
  });

  const weeklyForecast = [
    { day: "Today", condition: "Partly Cloudy", temp: "24°C", icon: Cloud, high: "28°", low: "18°" },
    { day: "Tomorrow", condition: "Sunny", temp: "26°C", icon: Sun, high: "30°", low: "20°" },
    { day: "Wed", condition: "Light Rain", temp: "22°C", icon: Droplets, high: "25°", low: "16°" },
    { day: "Thu", condition: "Sunny", temp: "25°C", icon: Sun, high: "29°", low: "19°" },
    { day: "Fri", condition: "Cloudy", temp: "23°C", icon: Cloud, high: "27°", low: "17°" }
  ];

  const cropData = {
    name: "Tomato",
    health: "85%",
    stage: "Flowering",
    daysToHarvest: 45,
    expectedYield: "2.5 tons"
  };

  const quickStats = [
    { label: "Active Crops", value: "3", icon: Leaf, color: "#22c55e" },
    { label: "Health Score", value: "85%", icon: Activity, color: "#3b82f6" },
    { label: "Yield Prediction", value: "2.5T", icon: TrendingUp, color: "#f59e0b" },
    { label: "Days to Harvest", value: "45", icon: Sun, color: "#ef4444" }
  ];

  return (
    <View className="flex-1 bg-gray-50">
      <StatusBar barStyle="light-content" backgroundColor="#16a34a" />
      
      {/* Header with Gradient */}
      <LinearGradient
        colors={['#16a34a', '#22c55e', '#4ade80']}
        style={{ paddingTop: insets.top + 20, paddingBottom: 24, paddingHorizontal: 20 }}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View className="flex-row justify-between items-center mb-4">
          <View>
            <Text className="text-2xl font-bold text-white mb-1">🌱 AgriSmart</Text>
            <View className="flex-row items-center">
              <MapPin size={14} color="#fff" />
              <Text className="text-white/90 text-sm ml-1">North Valley Farm</Text>
            </View>
          </View>
          <View className="flex-row space-x-2">
            <IconButton 
              icon={() => <Bell size={24} color="#fff" />}
              onPress={() => {}}
              className="bg-white/20 rounded-full"
            />
            <IconButton 
              icon={() => <Settings size={24} color="#fff" />}
              onPress={() => {}}
              className="bg-white/20 rounded-full"
            />
          </View>
        </View>
      </LinearGradient>

      <ScrollView 
        className="flex-1" 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        {/* Quick Stats */}
        <View className="px-4 -mt-6 mb-6">
          <View className="flex-row justify-between">
            {quickStats.map((stat, index) => (
              <Surface key={index} className="bg-white rounded-2xl p-4 flex-1 mx-1" elevation={2}>
                <View className="items-center">
                  <View className="bg-gray-100 rounded-full p-2 mb-2">
                    <stat.icon size={24} color={stat.color} />
                  </View>
                  <Text className="text-lg font-bold text-gray-800">{stat.value}</Text>
                  <Text className="text-xs text-gray-600 text-center">{stat.label}</Text>
                </View>
              </Surface>
            ))}
          </View>
        </View>

        {/* Current Weather Card */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <View className="flex-row items-center justify-between mb-4">
              <View className="flex-row items-center">
                <Cloud size={28} color="#22c55e" />
                <Title className="ml-3 text-gray-800 font-semibold">Current Weather</Title>
              </View>
              <Chip 
                icon={() => <ThermometerSun size={16} color="#f59e0b" />}
                className="bg-orange-50"
                textStyle={{ color: "#f59e0b", fontSize: 12 }}
              >
                {currentWeather.uvIndex}
              </Chip>
            </View>
            
            <View className="items-center mb-6">
              <Text className="text-5xl font-bold text-gray-800 mb-2">
                {currentWeather.temperature}
              </Text>
              <Text className="text-gray-600 text-lg">{currentWeather.condition}</Text>
            </View>
            
            <View className="flex-row justify-around bg-gray-50 rounded-xl p-4">
              <View className="items-center">
                <Droplets size={20} color="#3b82f6" />
                <Text className="text-gray-600 text-sm mt-1">Humidity</Text>
                <Text className="font-semibold text-gray-800">{currentWeather.humidity}</Text>
              </View>
              <View className="items-center">
                <Wind size={20} color="#6b7280" />
                <Text className="text-gray-600 text-sm mt-1">Wind</Text>
                <Text className="font-semibold text-gray-800">{currentWeather.wind}</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* 5-Day Forecast */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">5-Day Forecast</Title>
            {weeklyForecast.map((day, index) => (
              <View key={index} className="flex-row items-center justify-between py-3 border-b border-gray-100 last:border-b-0">
                <View className="flex-row items-center flex-1">
                  <day.icon size={24} color="#22c55e" />
                  <View className="ml-3 flex-1">
                    <Text className="font-semibold text-gray-800">{day.day}</Text>
                    <Text className="text-gray-600 text-sm">{day.condition}</Text>
                  </View>
                </View>
                <View className="flex-row items-center">
                  <Text className="font-bold text-gray-800 mr-2">{day.high}</Text>
                  <Text className="text-gray-500">{day.low}</Text>
                </View>
              </View>
            ))}
          </Card.Content>
        </Card>

        {/* Crop Monitoring Card */}
        <Card className="mx-4 mb-6 overflow-hidden" elevation={3}>
          <ImageBackground
            source={{ uri: 'https://images.unsplash.com/photo-1592419044706-39826d89274d?w=400&h=200&fit=crop' }}
            className="h-48"
            imageStyle={{ borderRadius: 12 }}
          >
            <LinearGradient
              colors={['transparent', 'rgba(0,0,0,0.8)']}
              className="flex-1 justify-end p-6"
            >
              <View className="flex-row items-end justify-between">
                <View className="flex-1">
                  <Text className="text-3xl font-bold text-white mb-1">{cropData.name}</Text>
                  <View className="flex-row items-center mb-1">
                    <Activity size={16} color="#22c55e" />
                    <Text className="text-green-400 font-semibold ml-2">{cropData.health} Health</Text>
                  </View>
                  <Text className="text-white/80 text-sm">Stage: {cropData.stage}</Text>
                  <Text className="text-white/70 text-xs">Expected: {cropData.expectedYield}</Text>
                </View>
                <Button 
                  mode="contained"
                  onPress={() => {}}
                  className="bg-green-600"
                  contentStyle={{ paddingVertical: 4 }}
                  labelStyle={{ fontSize: 12 }}
                  icon={() => <Eye size={16} color="#fff" />}
                >
                  View Details
                </Button>
              </View>
            </LinearGradient>
          </ImageBackground>
        </Card>

        {/* Quick Actions */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Quick Actions</Title>
            <View className="flex-row flex-wrap justify-between">
              {[
                { icon: Activity, label: "Health Check", color: "#22c55e", bg: "#f0fdf4" },
                { icon: TrendingUp, label: "Analytics", color: "#3b82f6", bg: "#eff6ff" },
                { icon: Leaf, label: "Recommendations", color: "#84cc16", bg: "#f7fee7" },
                { icon: Sun, label: "Weather Alerts", color: "#f59e0b", bg: "#fffbeb" }
              ].map((action, index) => (
                <TouchableOpacity 
                  key={index}
                  className="w-[48%] mb-3"
                  onPress={() => {}}
                >
                  <Surface 
                    className="p-4 rounded-xl items-center border border-gray-100"
                    style={{ backgroundColor: action.bg }}
                    elevation={1}
                  >
                    <action.icon size={28} color={action.color} />
                    <Text className="text-gray-800 font-medium text-center mt-2 text-sm">
                      {action.label}
                    </Text>
                  </Surface>
                </TouchableOpacity>
              ))}
            </View>
          </Card.Content>
        </Card>
      </ScrollView>
    </View>
  );
}
