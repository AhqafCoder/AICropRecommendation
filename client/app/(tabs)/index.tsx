import React, { useState, useEffect, useRef } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  Animated, 
  Dimensions,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert
} from 'react-native';
import { Mic, MicOff, Send, Leaf, Sun, Cloud, Droplets } from 'lucide-react-native';

const { width, height } = Dimensions.get('window');

// Define the Message interface
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
}

// Custom SVG Plant Icon Component
const PlantSVG = ({ size = 120, color = "#4CAF50" }) => (
  <View style={{ width: size, height: size, justifyContent: 'center', alignItems: 'center' }}>
    <View style={{
      width: size * 0.8,
      height: size * 0.8,
      borderRadius: size * 0.4,
      backgroundColor: `${color}20`,
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <Leaf size={size * 0.4} color={color} />
    </View>
  </View>
);

const CropRecommendationApp = () => {
  const [currentScreen, setCurrentScreen] = useState<'splash' | 'main'>('splash');
  const [inputText, setInputText] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([]); // Fixed: Proper type annotation
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Animation values
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.5)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  // Splash screen animation
  useEffect(() => {
    if (currentScreen === 'splash') {
      // Start animations
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.spring(scaleAnim, {
          toValue: 1,
          tension: 50,
          friction: 3,
          useNativeDriver: true,
        }),
        Animated.timing(slideAnim, {
          toValue: 0,
          duration: 800,
          delay: 500,
          useNativeDriver: true,
        })
      ]).start();

      // Continuous rotation for the plant icon
      Animated.loop(
        Animated.timing(rotateAnim, {
          toValue: 1,
          duration: 8000,
          useNativeDriver: true,
        })
      ).start();

      // Navigate to main screen after 3 seconds
      const timer = setTimeout(() => {
        setCurrentScreen('main');
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [currentScreen]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = { id: Date.now(), text: inputText, sender: 'user' }; // Fixed: Proper typing
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        `Based on your query "${userMessage.text}", I recommend considering crops like wheat, corn, or soybeans depending on your soil conditions and climate. For more specific recommendations, please provide details about your location, soil type, and current season.`,
        `For "${userMessage.text}", here are my suggestions: Consider legumes like beans or lentils for nitrogen-rich soil, or root vegetables like potatoes for well-drained areas.`,
        `Analyzing "${userMessage.text}"... I suggest drought-resistant crops like millet or sorghum if you're in an arid region, or rice varieties if you have access to irrigation.`
      ];
      
      const aiResponse: Message = { // Fixed: Proper typing
        id: Date.now() + 1,
        text: responses[Math.floor(Math.random() * responses.length)],
        sender: 'ai'
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 2000);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      Alert.alert("Recording Started", "Speak now for crop recommendations...");
      // In real implementation, start audio recording here
      setTimeout(() => {
        setIsRecording(false);
        setInputText("What crops grow best in sandy soil with moderate rainfall?");
        Alert.alert("Recording Complete", "Voice converted to text!");
      }, 3000);
    }
  };

  const spin = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  if (currentScreen === 'splash') {
    return (
      <View style={styles.splashContainer}>
        <Animated.View 
          style={[
            styles.splashContent,
            {
              opacity: fadeAnim,
              transform: [{ scale: scaleAnim }, { rotate: spin }]
            }
          ]}
        >
          <PlantSVG size={140} color="#4CAF50" />
        </Animated.View>
        
        <Animated.View 
          style={[
            styles.splashTextContainer,
            {
              opacity: fadeAnim,
              transform: [{ translateY: slideAnim }]
            }
          ]}
        >
          <Text style={styles.splashTitle}>CropAI</Text>
          <Text style={styles.splashSubtitle}>Smart Crop Recommendations</Text>
          <View style={styles.loadingDots}>
            <View style={styles.dot} />
            <View style={[styles.dot, { animationDelay: '0.2s' }]} />
            <View style={[styles.dot, { animationDelay: '0.4s' }]} />
          </View>
        </Animated.View>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView 
      style={styles.mainContainer} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <PlantSVG size={40} color="#4CAF50" />
          <Text style={styles.headerTitle}>CropAI Assistant</Text>
        </View>
        <View style={styles.weatherInfo}>
          <Sun size={16} color="#FFA726" />
          <Text style={styles.weatherText}>25°C</Text>
          <Droplets size={16} color="#42A5F5" />
          <Text style={styles.weatherText}>60%</Text>
        </View>
      </View>

      {/* Messages Area */}
      <ScrollView style={styles.messagesContainer} showsVerticalScrollIndicator={false}>
        {messages.length === 0 && (
          <View style={styles.welcomeContainer}>
            <PlantSVG size={80} color="#4CAF50" />
            <Text style={styles.welcomeTitle}>Welcome to CropAI!</Text>
            <Text style={styles.welcomeText}>
              Get personalized crop recommendations based on your soil, climate, and farming conditions.
            </Text>
            <View style={styles.suggestionContainer}>
              <Text style={styles.suggestionTitle}>Try asking:</Text>
              <TouchableOpacity 
                style={styles.suggestionBubble}
                onPress={() => setInputText("What crops are best for clay soil?")}
              >
                <Text style={styles.suggestionText}>What crops are best for clay soil?</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.suggestionBubble}
                onPress={() => setInputText("Recommend crops for winter season")}
              >
                <Text style={styles.suggestionText}>Recommend crops for winter season</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.suggestionBubble}
                onPress={() => setInputText("Best organic farming practices")}
              >
                <Text style={styles.suggestionText}>Best organic farming practices</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
        
        {messages.map((message) => (
          <View
            key={message.id}
            style={[
              styles.messageContainer,
              message.sender === 'user' ? styles.userMessage : styles.aiMessage
            ]}
          >
            <Text style={[
              styles.messageText,
              message.sender === 'user' ? styles.userMessageText : styles.aiMessageText
            ]}>
              {message.text}
            </Text>
          </View>
        ))}
        
        {isLoading && (
          <View style={styles.loadingContainer}>
            <View style={styles.typingIndicator}>
              <View style={styles.typingDot} />
              <View style={styles.typingDot} />
              <View style={styles.typingDot} />
            </View>
          </View>
        )}
      </ScrollView>

      {/* Input Area */}
      <View style={styles.inputContainer}>
        <View style={styles.inputWrapper}>
          <TextInput
            style={styles.textInput}
            placeholder="Ask about crops, soil, weather..."
            placeholderTextColor="#666"
            value={inputText}
            onChangeText={setInputText}
            multiline
            maxLength={500}
          />
          <View style={styles.inputActions}>
            <TouchableOpacity
              style={[
                styles.micButton,
                isRecording && styles.micButtonActive
              ]}
              onPress={toggleRecording}
            >
              {isRecording ? (
                <MicOff size={20} color={isRecording ? "#FFF" : "#4CAF50"} />
              ) : (
                <Mic size={20} color="#4CAF50" />
              )}
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.sendButton,
                !inputText.trim() && styles.sendButtonDisabled
              ]}
              onPress={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
            >
              <Send size={20} color={inputText.trim() ? "#FFF" : "#666"} />
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  // Splash Screen Styles
  splashContainer: {
    flex: 1,
    backgroundColor: '#0D1117',
    justifyContent: 'center',
    alignItems: 'center',
  },
  splashContent: {
    alignItems: 'center',
  },
  splashTextContainer: {
    alignItems: 'center',
    marginTop: 40,
  },
  splashTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 8,
  },
  splashSubtitle: {
    fontSize: 16,
    color: '#8B949E',
    marginBottom: 30,
  },
  loadingDots: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#4CAF50',
    marginHorizontal: 4,
    opacity: 0.3,
  },

  // Main Screen Styles
  mainContainer: {
    flex: 1,
    backgroundColor: '#0D1117',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 50,
    paddingBottom: 15,
    backgroundColor: '#161B22',
    borderBottomWidth: 1,
    borderBottomColor: '#21262D',
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#F0F6FC',
    marginLeft: 10,
  },
  weatherInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  weatherText: {
    color: '#8B949E',
    fontSize: 12,
    marginLeft: 4,
    marginRight: 12,
  },
  messagesContainer: {
    flex: 1,
    paddingHorizontal: 20,
  },
  welcomeContainer: {
    alignItems: 'center',
    paddingTop: 60,
    paddingBottom: 40,
  },
  welcomeTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#F0F6FC',
    marginTop: 20,
    marginBottom: 10,
  },
  welcomeText: {
    fontSize: 16,
    color: '#8B949E',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 30,
    paddingHorizontal: 20,
  },
  suggestionContainer: {
    width: '100%',
    alignItems: 'center',
  },
  suggestionTitle: {
    fontSize: 14,
    color: '#8B949E',
    marginBottom: 15,
  },
  suggestionBubble: {
    backgroundColor: '#21262D',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 20,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#30363D',
  },
  suggestionText: {
    color: '#4CAF50',
    fontSize: 14,
  },
  messageContainer: {
    marginVertical: 8,
    maxWidth: '80%',
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#4CAF50',
    borderRadius: 18,
    borderBottomRightRadius: 4,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  aiMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#21262D',
    borderRadius: 18,
    borderBottomLeftRadius: 4,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: '#30363D',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userMessageText: {
    color: '#FFF',
  },
  aiMessageText: {
    color: '#F0F6FC',
  },
  loadingContainer: {
    alignSelf: 'flex-start',
    marginVertical: 8,
  },
  typingIndicator: {
    flexDirection: 'row',
    backgroundColor: '#21262D',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 18,
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: '#30363D',
  },
  typingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#8B949E',
    marginRight: 4,
    opacity: 0.6,
  },
  inputContainer: {
    paddingHorizontal: 20,
    paddingVertical: 20,
    backgroundColor: '#161B22',
    borderTopWidth: 1,
    borderTopColor: '#21262D',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    backgroundColor: '#21262D',
    borderRadius: 24,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderWidth: 1,
    borderColor: '#30363D',
    minHeight: 48,
  },
  textInput: {
    flex: 1,
    color: '#F0F6FC',
    fontSize: 16,
    maxHeight: 100,
    paddingVertical: 8,
  },
  inputActions: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 8,
  },
  micButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#0D1117',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  micButtonActive: {
    backgroundColor: '#D32F2F',
    borderColor: '#D32F2F',
  },
  sendButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#30363D',
  },
});

export default CropRecommendationApp;
