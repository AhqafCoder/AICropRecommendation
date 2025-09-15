# 🌾 HackBhoomi2025 - Agricultural Intelligence Mobile App

A comprehensive **React Native mobile application** built with **Expo** and **TypeScript** for intelligent agricultural management. Features AI-powered crop disease detection, real-time analytics, and comprehensive farm management tools designed for modern farmers.

## 🎯 **Key Features**

### **📱 5 Core Screens**
- **🏠 Home Dashboard** - Real-time weather, farm overview, and quick actions
- **📷 AI Scan** - Disease detection, plant identification, and soil analysis
- **📊 Analytics** - Crop health metrics, growth tracking, and trend analysis
- **🔍 Explore** - Agricultural knowledge base and recommendations
- **🛒 Shop** - Agricultural products and marketplace
- **👤 Profile** - User settings and farm management

### **🤖 AI-Powered Features**
- **Disease Detection** - Advanced image recognition for plant diseases
- **Plant Identification** - Real-time species recognition
- **Soil Analysis** - Visual soil condition assessment
- **Health Monitoring** - Crop growth and vitality tracking

### **📊 Smart Analytics**
- **Real-time Metrics** - Live crop health monitoring (87% overall health)
- **Growth Tracking** - Progressive growth rate analysis (92% efficiency)
- **Weather Integration** - Environmental condition monitoring
- **Predictive Insights** - Data-driven farming recommendations

### **🎨 Modern UI/UX**
- **Material Design 3** - React Native Paper components
- **NativeWind** - Tailwind CSS for React Native styling
- **Lucide Icons** - Beautiful, consistent iconography
- **Responsive Design** - Optimized for all screen sizes
- **Dark/Light Theme** - Automatic theme switching

## 🛠️ **Tech Stack**

### **Core Framework**
- **React Native 0.79.6** - Cross-platform mobile development
- **Expo SDK 53** - Development platform and build tools
- **TypeScript 5.8.3** - Type-safe development
- **Expo Router 5.1.5** - File-based navigation system

### **UI & Styling**
- **React Native Paper 5.14.5** - Material Design components
- **NativeWind 4.1.23** - Tailwind CSS for React Native
- **Lucide React Native 0.542.0** - Modern icon library
- **Expo Linear Gradient** - Beautiful gradient backgrounds

### **Navigation & UX**
- **React Navigation 7.1.6** - Native navigation
- **React Native Gesture Handler** - Smooth touch interactions
- **React Native Reanimated 3.17.4** - High-performance animations
- **Expo Haptics** - Tactile feedback

### **Development Tools**
- **ESLint 9.25.0** - Code quality and consistency
- **Babel** - JavaScript compilation
- **Metro** - React Native bundler
- **TypeScript** - Static type checking

## 📱 **Screen-by-Screen Features**

### **🏠 Home Screen (`index.tsx`)**
**Smart Farm Dashboard**
- **Real-time Weather Widget**: Temperature (24°C), humidity (68%), wind speed
- **Quick Action Cards**: Instant access to scanning, analysis, and settings
- **Farm Status Overview**: Current conditions and alerts
- **Weather Integration**: Location-based environmental data
- **Gradient UI**: Beautiful visual design with farm imagery

**Key Components:**
- Live weather monitoring with UV index
- Farm location tracking (North Valley)
- Quick navigation to all app features
- Status indicators for farm health

### **📷 Scan Screen (`scan.tsx`)**
**AI-Powered Visual Analysis**
- **Disease Detection**: Advanced plant disease identification
- **Plant Identification**: Species recognition and classification
- **Soil Analysis**: Visual soil condition assessment
- **Multi-mode Scanning**: Toggle between detection types

**Scan Capabilities:**
- **Disease Detection** (Red indicator) - Identify plant diseases and pathogens
- **Plant Identification** (Green indicator) - Recognize plant species and varieties
- **Soil Analysis** (Blue indicator) - Assess soil health and composition

**Features:**
- Camera integration for real-time scanning
- Upload from gallery support
- Instant AI-powered results
- Visual feedback and animations

### **📊 Analysis Screen (`analysis.tsx`)**
**Comprehensive Crop Analytics**
- **Health Metrics Dashboard**: Overall health (87%), growth rate (92%)
- **Trend Analysis**: Weekly, monthly, seasonal data
- **Performance Indicators**: Color-coded status tracking
- **Progress Visualization**: Interactive charts and graphs

**Key Metrics:**
- **Overall Health**: 87% (Excellent status, +5% improvement)
- **Growth Rate**: 92% (Good status, +12% improvement)
- **Environmental Tracking**: Temperature, humidity, soil conditions
- **Predictive Analytics**: Future growth projections

**Analytics Features:**
- Time period selection (week/month/season)
- Segmented button controls
- Progress bars and indicators
- Trend comparison charts

### **🔍 Explore Screen (`explore.tsx`)**
**Agricultural Knowledge Hub**
- **Knowledge Base**: Comprehensive farming information
- **Best Practices**: Expert recommendations and guides
- **Seasonal Advice**: Time-specific farming tips
- **Community Insights**: Shared farmer experiences

### **🛒 Shop Screen (`shop.tsx`)**
**Agricultural Marketplace**
- **Product Catalog**: Seeds, fertilizers, tools, equipment
- **Smart Recommendations**: AI-suggested products based on farm data
- **Price Comparison**: Best deals and offers
- **Order Management**: Purchase tracking and delivery

### **👤 Profile Screen (`profile.tsx`)**
**User & Farm Management**
- **Personal Settings**: User preferences and configurations
- **Farm Details**: Property information and crop management
- **Historical Data**: Past seasons and performance records
- **Account Management**: Security and subscription settings

## 📁 **Project Structure**

```
androidapp/
├── app/                          # Expo Router file-based navigation
│   ├── _layout.tsx              # Root layout with theme provider
│   ├── +not-found.tsx           # 404 error screen
│   └── (tabs)/                  # Tab-based navigation group
│       ├── _layout.tsx          # Tab navigation layout
│       ├── index.tsx            # 🏠 Home screen (dashboard)
│       ├── scan.tsx             # 📷 AI scan screen
│       ├── analysis.tsx         # 📊 Analytics screen
│       ├── explore.tsx          # 🔍 Explore screen
│       ├── shop.tsx             # 🛒 Shop screen
│       └── profile.tsx          # 👤 Profile screen
├── components/                   # Reusable UI components
│   ├── common/                  # Shared components
│   │   └── Header/              # Navigation header
│   ├── ui/                      # UI-specific components
│   │   ├── IconSymbol.tsx       # Platform-specific icons
│   │   └── TabBarBackground.tsx # Custom tab bar styling
│   ├── Collapsible.tsx         # Expandable content
│   ├── ExternalLink.tsx        # External URL handler
│   ├── HapticTab.tsx           # Touch feedback tabs
│   ├── ParallaxScrollView.tsx  # Smooth scrolling effects
│   ├── ThemedText.tsx          # Theme-aware text component
│   ├── ThemedView.tsx          # Theme-aware view component
│   └── WeatherWidget.tsx       # Weather display component
├── constants/                   # App constants and configuration
│   └── Colors.ts               # Theme color definitions
├── hooks/                      # Custom React hooks
│   ├── useColorScheme.ts       # Theme detection hook
│   ├── useColorScheme.web.ts   # Web-specific theme hook
│   └── useThemeColor.ts        # Theme color hook
├── assets/                     # Static assets
│   ├── fonts/                  # Custom fonts
│   └── images/                 # App icons and images
├── scripts/                    # Build and utility scripts
│   └── reset-project.js        # Project reset utility
├── .expo/                      # Expo configuration and cache
├── package.json                # Dependencies and scripts
├── app.json                    # Expo app configuration
├── tailwind.config.js          # NativeWind styling configuration
├── tsconfig.json              # TypeScript configuration
├── babel.config.js            # Babel transpilation config
├── metro.config.js            # Metro bundler configuration
└── global.css                 # Global styles for NativeWind
```

## 🎨 **Design System**

### **Color Palette (Tailwind Configuration)**
- **Primary Green**: Agricultural theme with shades from 50-900
- **Secondary Gray**: Professional UI elements
- **Accent Colors**: Status indicators and highlights
- **Semantic Colors**: Success, warning, error states

### **Component Architecture**
- **Screen Components**: Full-screen views with navigation
- **Common Components**: Reusable UI elements
- **Themed Components**: Auto-switching dark/light mode
- **Icon System**: Lucide icons with consistent sizing

### **Typography & Spacing**
- **Custom Fonts**: SpaceMono for headers
- **Responsive Sizing**: Adaptive to different screen sizes
- **Consistent Spacing**: Tailwind spacing scale
- **Accessibility**: WCAG-compliant color contrasts

## 🚀 **Navigation Architecture**

### **Expo Router File-Based System**
- **Root Layout**: App-wide configuration and providers
- **Tab Navigation**: Bottom tab bar with 5 main screens
- **Stack Navigation**: Nested navigation within tabs
- **Type-Safe Routing**: TypeScript-powered navigation

### **Tab Bar Features**
- **Haptic Feedback**: Touch response on tab selection
- **Custom Styling**: Elevated design with rounded corners
- **Active States**: Visual feedback for current screen
- **Icon Integration**: Lucide icons with color themes

## 🚀 **Getting Started**

### **📋 Prerequisites**
- **Node.js** 18+ (LTS recommended)
- **npm** or **yarn** package manager
- **Expo CLI** (`npm install -g @expo/cli`)
- **Android Studio** (for Android development)
- **Xcode** (for iOS development - Mac only)

### **⚡ Quick Start**

#### **1. Install Dependencies**
```bash
# Install project dependencies
npm install

# Or using yarn
yarn install
```

#### **2. Start Development Server**
```bash
# Start Expo development server
npm start

# Or using yarn
yarn start

# Alternative: Start with specific platform
npm run android    # Open on Android emulator
npm run ios        # Open on iOS simulator (Mac only)
npm run web        # Open in web browser
```

#### **3. Development Options**
When you run `npm start`, you'll get options to:
- **📱 Open on physical device** - Scan QR code with Expo Go app
- **🤖 Android Emulator** - Requires Android Studio setup
- **📱 iOS Simulator** - Requires Xcode (Mac only)
- **🌐 Web Browser** - React Native Web support

### **📱 Device Setup**

#### **Physical Device Testing**
1. **Install Expo Go** from App Store/Play Store
2. **Run** `npm start` in project directory
3. **Scan QR code** with Expo Go app
4. **App loads** automatically with hot reload

#### **Android Emulator Setup**
1. **Install Android Studio**
2. **Create AVD** (Android Virtual Device)
3. **Start emulator** before running `npm run android`
4. **App installs** automatically

#### **iOS Simulator Setup** (Mac only)
1. **Install Xcode** from Mac App Store
2. **Open Xcode** and install iOS Simulator
3. **Run** `npm run ios` to open in simulator
4. **App builds** and installs automatically

## 🛠️ **Development Workflow**

### **📝 Available Scripts**

```bash
# Development
npm start                 # Start Expo development server
npm run android          # Run on Android (emulator/device)
npm run ios             # Run on iOS (simulator/device)
npm run web             # Run in web browser

# Code Quality
npm run lint            # Run ESLint for code quality
npm run reset-project   # Reset to fresh project state

# Building & Deployment
npx expo build:android  # Build Android APK/AAB
npx expo build:ios      # Build iOS IPA (Mac only)
npx expo export         # Export for production deployment
```

### **🔧 Development Tools & Features**

#### **Hot Reload & Fast Refresh**
- **Automatic Updates**: Code changes reflect instantly
- **State Preservation**: Component state maintained during updates
- **Error Overlay**: In-app error messages with stack traces

#### **TypeScript Integration**
- **Type Safety**: Full TypeScript support with strict mode
- **IntelliSense**: Auto-completion and error detection
- **Type Checking**: Compile-time error prevention

#### **Styling with NativeWind**
```tsx
// Use Tailwind classes directly in React Native
<View className="flex-1 bg-primary-50 p-4">
  <Text className="text-2xl font-bold text-primary-700">
    Agricultural Intelligence
  </Text>
</View>
```

#### **Navigation with Expo Router**
```tsx
// File-based routing - create files in app/ directory
// app/(tabs)/scan.tsx automatically creates /scan route
import { Link } from 'expo-router';

<Link href="/scan" className="text-primary-600">
  Go to Scan Screen
</Link>
```

### **🎨 Customization & Theming**

#### **Theme Configuration**
```typescript
// constants/Colors.ts
export const Colors = {
  light: {
    primary: '#22c55e',
    background: '#ffffff',
    surface: '#f8fafc',
  },
  dark: {
    primary: '#4ade80',
    background: '#0f172a',
    surface: '#1e293b',
  }
};
```

#### **Component Styling**
```tsx
// Using React Native Paper with custom theme
import { Card, Title } from 'react-native-paper';

<Card className="m-4 bg-white shadow-lg">
  <Title className="text-primary-700 p-4">
    Farm Analytics
  </Title>
</Card>
```

## 📦 **Building & Deployment**

### **🔨 Production Builds**

#### **Android Build**
```bash
# Create development build
npx expo run:android

# Create production build
eas build -p android

# Create APK for testing
eas build -p android --profile preview
```

#### **iOS Build** (Mac only)
```bash
# Create development build
npx expo run:ios

# Create production build
eas build -p ios

# Create TestFlight build
eas build -p ios --profile preview
```

### **🚀 Deployment Options**

#### **Expo Application Services (EAS)**
```bash
# Install EAS CLI
npm install -g eas-cli

# Configure project
eas build:configure

# Build for both platforms
eas build --platform all
```

#### **Over-the-Air Updates**
```bash
# Publish updates instantly
npx expo publish

# Update specific release channel
npx expo publish --release-channel production
```

## 🧪 **Testing & Quality**

### **Code Quality Tools**
- **ESLint**: Consistent code formatting and error detection
- **TypeScript**: Static type checking and IntelliSense
- **Expo CLI**: Built-in development tools and debugging

### **Testing Strategy**
- **Manual Testing**: Expo Go app for rapid iteration
- **Emulator Testing**: Android/iOS emulator validation
- **Device Testing**: Real device performance testing
- **Cross-Platform**: Ensure consistency across platforms

## 📚 **Resources & Documentation**

### **Official Documentation**
- **[Expo Documentation](https://docs.expo.dev/)** - Complete Expo framework guide
- **[React Native Docs](https://reactnative.dev/docs/getting-started)** - Core React Native concepts
- **[Expo Router](https://docs.expo.dev/router/introduction/)** - File-based navigation
- **[React Native Paper](https://reactnativepaper.com/)** - Material Design components

### **Styling & UI**
- **[NativeWind](https://www.nativewind.dev/)** - Tailwind CSS for React Native
- **[Tailwind CSS](https://tailwindcss.com/docs)** - Utility-first CSS framework
- **[Lucide Icons](https://lucide.dev/)** - Beautiful icon library

### **Development Tools**
- **[Android Studio](https://developer.android.com/studio)** - Android development environment
- **[Xcode](https://developer.apple.com/xcode/)** - iOS development (Mac only)
- **[Expo Go](https://expo.dev/go)** - Mobile app for testing

## 🎯 **Project Status**

### **✅ Completed Features**
- **Tab-based Navigation**: 5 main screens with routing
- **Modern UI Design**: Material Design 3 with NativeWind
- **Home Dashboard**: Weather integration and quick actions
- **Scan Interface**: Multi-mode AI scanning preparation
- **Analytics Dashboard**: Comprehensive metrics display
- **TypeScript Setup**: Full type safety implementation
- **Cross-platform Support**: Android, iOS, and Web

### **🚧 In Development**
- **AI Integration**: Backend API connections for scanning
- **Real-time Data**: Live sensor data integration
- **User Authentication**: Login and profile management
- **Cloud Sync**: Data synchronization across devices
- **Push Notifications**: Real-time alerts and updates

### **🎯 Future Enhancements**
- **Offline Mode**: Local data storage and sync
- **Advanced Analytics**: Machine learning insights
- **Community Features**: Farmer networking and sharing
- **IoT Integration**: Smart sensor data collection
- **Marketplace**: In-app purchasing and transactions

## 📱 **App Information**

- **Name**: HackBhoomi2025 Agricultural Intelligence
- **Version**: 1.0.0
- **Package**: com.ahqafcoder.client
- **Minimum OS**: iOS 13+, Android 7.0+
- **Bundle Size**: ~50MB (optimized for mobile networks)
- **Offline Support**: Planned for future releases
