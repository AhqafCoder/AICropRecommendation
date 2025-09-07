import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Cloud, Sun, CloudRain, Wind, Droplets } from 'lucide-react-native';

interface WeatherWidgetProps {
  temperature: string;
  condition: string;
  humidity: string;
  windSpeed: string;
  compact?: boolean;
}

const getWeatherIcon = (condition: string) => {
  const lowerCondition = condition.toLowerCase();
  if (lowerCondition.includes('sunny') || lowerCondition.includes('clear')) {
    return <Sun size={24} color="#FFA726" />;
  } else if (lowerCondition.includes('rain')) {
    return <CloudRain size={24} color="#42A5F5" />;
  } else if (lowerCondition.includes('cloud')) {
    return <Cloud size={24} color="#78909C" />;
  }
  return <Cloud size={24} color="#78909C" />;
};

export default function WeatherWidget({ 
  temperature, 
  condition, 
  humidity, 
  windSpeed, 
  compact = false 
}: WeatherWidgetProps) {
  if (compact) {
    return (
      <View style={styles.compactContainer}>
        {getWeatherIcon(condition)}
        <Text style={styles.compactTemp}>{temperature}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        {getWeatherIcon(condition)}
        <Text style={styles.title}>Current Weather</Text>
      </View>
      
      <View style={styles.mainInfo}>
        <Text style={styles.temperature}>{temperature}</Text>
        <Text style={styles.condition}>{condition}</Text>
      </View>
      
      <View style={styles.details}>
        <View style={styles.detailItem}>
          <Droplets size={16} color="#2196F3" />
          <Text style={styles.detailText}>Humidity: {humidity}</Text>
        </View>
        <View style={styles.detailItem}>
          <Wind size={16} color="#9E9E9E" />
          <Text style={styles.detailText}>Wind: {windSpeed}</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  compactContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 12,
    color: '#333',
  },
  mainInfo: {
    alignItems: 'center',
    marginBottom: 20,
  },
  temperature: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#333',
  },
  condition: {
    fontSize: 16,
    color: '#666',
    marginTop: 4,
  },
  compactTemp: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginLeft: 8,
  },
  details: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  detailText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#666',
  },
});
