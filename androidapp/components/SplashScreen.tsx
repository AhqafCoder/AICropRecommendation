import React, { useEffect } from 'react';
import { View, Text, Animated, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Sprout } from 'lucide-react-native';

const { width, height } = Dimensions.get('window');

interface SplashScreenProps {
  onFinish: () => void;
}

export default function SplashScreen({ onFinish }: SplashScreenProps) {
  const fadeAnim = new Animated.Value(0);
  const scaleAnim = new Animated.Value(0.8);

  useEffect(() => {
    // Animate logo appearance
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 1000,
        useNativeDriver: true,
      }),
    ]).start();

    // Hide splash screen after 3 seconds
    const timer = setTimeout(() => {
      onFinish();
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <LinearGradient
      colors={['#22c55e', '#16a34a', '#15803d']}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        width,
        height,
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 9999,
      }}
    >
      <Animated.View
        style={{
          opacity: fadeAnim,
          transform: [{ scale: scaleAnim }],
          alignItems: 'center',
        }}
      >
        <View
          style={{
            backgroundColor: 'rgba(255, 255, 255, 0.2)',
            borderRadius: 80,
            padding: 30,
            marginBottom: 20,
          }}
        >
          <Sprout size={60} color="white" />
        </View>
        
        <Text
          style={{
            fontSize: 32,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: 8,
            textAlign: 'center',
          }}
        >
          AgriSmart
        </Text>
        
        <Text
          style={{
            fontSize: 16,
            color: 'rgba(255, 255, 255, 0.9)',
            textAlign: 'center',
            marginBottom: 40,
          }}
        >
          Smart Farming Solutions
        </Text>
        
        <View
          style={{
            width: 40,
            height: 4,
            backgroundColor: 'rgba(255, 255, 255, 0.6)',
            borderRadius: 2,
          }}
        />
      </Animated.View>
    </LinearGradient>
  );
}
