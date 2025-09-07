import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { 
  Card, 
  Title, 
  Paragraph, 
  Button, 
  Avatar, 
  Surface,
  List,
  Divider,
  Switch,
  IconButton
} from 'react-native-paper';
import { 
  User, 
  Settings, 
  MapPin, 
  Phone, 
  Mail, 
  Bell,
  Shield,
  HelpCircle,
  LogOut,
  Edit3,
  Camera,
  Award,
  TrendingUp,
  Calendar
} from 'lucide-react-native';

export default function ProfileScreen() {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [locationEnabled, setLocationEnabled] = useState(true);

  const profileStats = [
    { label: "Farms Managed", value: "3", icon: MapPin, color: "#22c55e" },
    { label: "Years Experience", value: "8", icon: Calendar, color: "#3b82f6" },
    { label: "Success Rate", value: "94%", icon: TrendingUp, color: "#f59e0b" },
    { label: "Achievements", value: "12", icon: Award, color: "#ef4444" }
  ];

  const menuItems = [
    { icon: Edit3, title: "Edit Profile", subtitle: "Update your personal information", onPress: () => {} },
    { icon: Bell, title: "Notifications", subtitle: "Manage alert preferences", onPress: () => {}, hasSwitch: true, switchValue: notificationsEnabled, onSwitchToggle: setNotificationsEnabled },
    { icon: MapPin, title: "Location Services", subtitle: "Weather and location data", onPress: () => {}, hasSwitch: true, switchValue: locationEnabled, onSwitchToggle: setLocationEnabled },
    { icon: Shield, title: "Privacy & Security", subtitle: "Account security settings", onPress: () => {} },
    { icon: HelpCircle, title: "Help & Support", subtitle: "FAQs and contact support", onPress: () => {} },
    { icon: Settings, title: "App Settings", subtitle: "Preferences and configurations", onPress: () => {} }
  ];

  return (
    <View className="flex-1 bg-gray-50">
      <StatusBar barStyle="light-content" backgroundColor="#16a34a" />
      
      {/* Header with Gradient */}
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="pt-12 pb-8"
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View className="items-center">
          <View className="relative mb-4">
            <Avatar.Text 
              size={100} 
              label="JF" 
              className="bg-white/20"
              labelStyle={{ color: '#fff', fontSize: 24, fontWeight: 'bold' }}
            />
            <TouchableOpacity className="absolute bottom-0 right-0 bg-white rounded-full p-2">
              <Camera size={20} color="#22c55e" />
            </TouchableOpacity>
          </View>
          <Text className="text-2xl font-bold text-white mb-1">John Farmer</Text>
          <Text className="text-white/80 text-base mb-1">Senior Agricultural Specialist</Text>
          <View className="flex-row items-center">
            <MapPin size={16} color="#fff" />
            <Text className="text-white/70 ml-1">North Valley, California</Text>
          </View>
        </View>
      </LinearGradient>

      <ScrollView 
        className="flex-1" 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        {/* Profile Stats */}
        <View className="px-4 -mt-6 mb-6">
          <View className="flex-row justify-between">
            {profileStats.map((stat, index) => (
              <Surface key={index} className="bg-white rounded-2xl p-4 flex-1 mx-1" elevation={2}>
                <View className="items-center">
                  <View className="bg-gray-100 rounded-full p-2 mb-2">
                    <stat.icon size={20} color={stat.color} />
                  </View>
                  <Text className="text-lg font-bold text-gray-800">{stat.value}</Text>
                  <Text className="text-xs text-gray-600 text-center">{stat.label}</Text>
                </View>
              </Surface>
            ))}
          </View>
        </View>

        {/* Contact Information */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Contact Information</Title>
            
            <View className="flex-row items-center py-3 border-b border-gray-100">
              <View className="bg-blue-50 rounded-full p-2 mr-4">
                <Phone size={20} color="#3b82f6" />
              </View>
              <View className="flex-1">
                <Text className="text-gray-800 font-medium">Phone</Text>
                <Text className="text-gray-600">+1 (555) 123-4567</Text>
              </View>
            </View>

            <View className="flex-row items-center py-3 border-b border-gray-100">
              <View className="bg-green-50 rounded-full p-2 mr-4">
                <Mail size={20} color="#22c55e" />
              </View>
              <View className="flex-1">
                <Text className="text-gray-800 font-medium">Email</Text>
                <Text className="text-gray-600">john.farmer@email.com</Text>
              </View>
            </View>

            <View className="flex-row items-center py-3">
              <View className="bg-purple-50 rounded-full p-2 mr-4">
                <MapPin size={20} color="#8b5cf6" />
              </View>
              <View className="flex-1">
                <Text className="text-gray-800 font-medium">Address</Text>
                <Text className="text-gray-600">123 Farm Road, Agricultural District</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Settings Menu */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Settings</Title>
            
            {menuItems.map((item, index) => (
              <TouchableOpacity
                key={index}
                className="flex-row items-center py-4 border-b border-gray-100 last:border-b-0"
                onPress={item.onPress}
              >
                <View className="bg-gray-50 rounded-full p-2 mr-4">
                  <item.icon size={20} color="#6b7280" />
                </View>
                <View className="flex-1">
                  <Text className="text-gray-800 font-medium">{item.title}</Text>
                  <Text className="text-gray-500 text-sm">{item.subtitle}</Text>
                </View>
                {item.hasSwitch ? (
                  <Switch
                    value={item.switchValue}
                    onValueChange={item.onSwitchToggle}
                    trackColor={{ false: '#e5e7eb', true: '#bbf7d0' }}
                    thumbColor={item.switchValue ? '#22c55e' : '#f3f4f6'}
                  />
                ) : (
                  <View className="bg-gray-100 rounded-full p-1">
                    <Text className="text-gray-400">›</Text>
                  </View>
                )}
              </TouchableOpacity>
            ))}
          </Card.Content>
        </Card>

        {/* Farm Performance Summary */}
        <Card className="mx-4 mb-6 bg-white" elevation={3}>
          <Card.Content className="p-6">
            <Title className="text-gray-800 font-semibold mb-4">Recent Performance</Title>
            
            <View className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-4 mb-4">
              <View className="flex-row justify-between items-center">
                <View>
                  <Text className="text-gray-800 font-semibold text-lg">This Month</Text>
                  <Text className="text-gray-600">Crop Health Average</Text>
                </View>
                <View className="items-end">
                  <Text className="text-3xl font-bold text-green-600">87%</Text>
                  <Text className="text-green-600 text-sm">↑ 5% from last month</Text>
                </View>
              </View>
            </View>

            <View className="flex-row justify-between">
              <View className="bg-blue-50 rounded-xl p-3 flex-1 mr-2">
                <Text className="text-blue-600 font-semibold">Water Usage</Text>
                <Text className="text-2xl font-bold text-blue-800">1,240L</Text>
                <Text className="text-blue-600 text-xs">This week</Text>
              </View>
              <View className="bg-orange-50 rounded-xl p-3 flex-1 ml-2">
                <Text className="text-orange-600 font-semibold">Yield Forecast</Text>
                <Text className="text-2xl font-bold text-orange-800">94%</Text>
                <Text className="text-orange-600 text-xs">Expected</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Logout Button */}
        <View className="mx-4 mb-6">
          <Button
            mode="outlined"
            onPress={() => {}}
            className="border-red-200 py-2"
            labelStyle={{ color: '#ef4444', fontSize: 16, fontWeight: '600' }}
            icon={() => <LogOut size={20} color="#ef4444" />}
            contentStyle={{ paddingVertical: 8 }}
          >
            Sign Out
          </Button>
        </View>
      </ScrollView>
    </View>
  );
}
