# 🌾 HackBhoomi2025 - Smart Agricultural Web Platform

A comprehensive **Next.js 15 web application** featuring AI-powered crop disease detection, intelligent farming recommendations, and agricultural marketplace functionality. Built with modern technologies including **TypeScript**, **Tailwind CSS**, and **Clerk authentication** to provide farmers with cutting-edge agricultural intelligence tools.

## 🎯 **Key Features**

### **🤖 AI-Powered Agriculture**
- **Crop Recommendations** - Personalized suggestions based on soil, weather, and historical data
- **Disease Detection** - Real-time image analysis for plant disease identification
- **Market Analytics** - Data-driven insights for optimal farming decisions
- **Yield Predictions** - Advanced forecasting for harvest planning

### **📊 Smart Dashboard**
- **Farm Analytics** - Comprehensive metrics and performance tracking
- **Health Monitoring** - Real-time crop health assessment
- **Weather Integration** - Environmental data and alerts
- **Market Insights** - Price trends and demand analysis

### **🛒 Agricultural Marketplace**
- **Product Catalog** - Seeds, fertilizers, equipment, and tools
- **Smart Recommendations** - AI-suggested products based on farm data
- **Vendor Management** - Seller profiles and ratings
- **Order Processing** - Complete transaction management

### **🔐 User Experience**
- **Secure Authentication** - Clerk-powered user management
- **Responsive Design** - Optimized for desktop, tablet, and mobile
- **Modern UI/UX** - Beautiful interface with Radix UI components
- **Real-time Updates** - Live data synchronization

## 🛠️ **Tech Stack**

### **Frontend Framework**
- **Next.js 15.5.2** - React framework with App Router and Server Components
- **React 19.1.0** - Latest React with concurrent features
- **TypeScript 5** - Type-safe development with strict mode
- **Turbopack** - Ultra-fast bundler for development and production

### **Styling & UI**
- **Tailwind CSS 4** - Utility-first CSS framework with custom configuration
- **Radix UI** - Unstyled, accessible UI primitives
- **Lucide React 0.542.0** - Beautiful, customizable icons
- **Class Variance Authority** - Component variant management

### **Authentication & Security**
- **Clerk 6.32.0** - Complete authentication solution
- **Middleware Protection** - Route-based access control
- **Session Management** - Secure user state handling

### **Data Visualization**
- **Recharts 3.2.0** - Composable charting library
- **Interactive Charts** - Analytics and market data visualization
- **Responsive Graphs** - Mobile-optimized data displays

### **Development Tools**
- **ESLint 9** - Code quality and consistency
- **PostCSS** - CSS processing and optimization
- **Concurrent Scripts** - Multi-service development workflow

## 📱 **Application Features & Pages**

### **🏠 Landing Page (`/`)**
**Smart Agricultural Intelligence Hub**
- **Hero Section** - AI-powered crop recommendations introduction
- **Feature Showcase** - Disease detection, analytics, marketplace highlights
- **Call-to-Action** - User registration and platform access
- **Responsive Design** - Mobile-optimized landing experience

**Key Components:**
- Gradient hero section with animated elements
- Feature cards with icons and descriptions
- Navigation header with authentication
- Footer with links and information

### **🔐 Authentication System**
**Secure User Management**
- **Sign Up** (`/sign-up`) - New user registration with Clerk
- **Sign In** (`/sign-in`) - Secure login with multiple providers
- **Profile Management** - User settings and preferences
- **Session Handling** - Automatic redirects and state management

### **📊 Dashboard (`/dashboard`)**
**Comprehensive Farm Management Hub**

#### **Main Dashboard** (`/dashboard`)
- **Farm Overview** - Key metrics and health indicators
- **Quick Actions** - Rapid access to core features
- **Weather Widget** - Current conditions and forecasts
- **Recent Activity** - Latest detections and recommendations

#### **Analytics** (`/dashboard/analytics`)
- **Performance Metrics** - Crop health and yield analytics
- **Market Trends** - Price analysis and demand forecasting
- **Historical Data** - Seasonal performance comparison
- **Interactive Charts** - Recharts-powered visualizations

#### **Disease Detection** (`/dashboard/detection`)
- **Image Upload** - Camera and file upload support
- **AI Analysis** - Real-time disease identification
- **Treatment Recommendations** - Expert-guided solutions
- **Detection History** - Past diagnoses and outcomes

#### **Crop Recommendations** (`/dashboard/recommend`)
- **Soil Analysis** - NPK and pH-based suggestions
- **Weather Integration** - Climate-optimized recommendations
- **Market Insights** - Profit-driven crop selection
- **Seasonal Planning** - Year-round farming strategy

#### **Marketplace** (`/dashboard/marketplace`)
- **Product Browse** - Agricultural supplies catalog
- **Advanced Search** - Category and filter-based discovery
- **Vendor Profiles** - Seller information and ratings
- **Purchase Management** - Order tracking and history

#### **Health Monitoring** (`/dashboard/health`)
- **Crop Status** - Real-time health assessment
- **Disease Alerts** - Early warning system
- **Growth Tracking** - Development stage monitoring
- **Intervention Recommendations** - Preventive measures

#### **Settings** (`/dashboard/settings`)
- **Profile Management** - User information updates
- **Farm Configuration** - Property and crop settings
- **Notification Preferences** - Alert customization
- **Privacy Controls** - Data and sharing settings

### **🔍 Dedicated Feature Pages**

#### **Detection Portal** (`/detection`)
- **Standalone Disease Detection** - Public access tool
- **Enhanced Upload Interface** - Drag-and-drop functionality
- **Detailed Results** - Comprehensive analysis reports
- **Export Options** - PDF and image result sharing

#### **Marketplace Hub** (`/marketplace`)
- **Full Catalog View** - Complete product marketplace
- **Advanced Filtering** - Multi-criteria product search
- **Comparison Tools** - Side-by-side product analysis
- **Bulk Ordering** - Quantity-based purchasing

#### **Analytics Center** (`/analytics`)
- **Market Intelligence** - Regional and global trends
- **Predictive Modeling** - Future market conditions
- **Custom Reports** - User-defined analytics
- **Data Export** - CSV and API access

#### **Recommendation Engine** (`/recommend`)
- **Comprehensive Analysis** - Multi-factor crop suggestions
- **Interactive Form** - Step-by-step data collection
- **Scenario Planning** - What-if analysis tools
- **Implementation Guides** - Detailed farming instructions

## 🏗️ **Project Structure**

```
client/
├── src/
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx          # Root layout with providers
│   │   ├── page.tsx            # Landing page
│   │   ├── globals.css         # Global styles and Tailwind
│   │   ├── analytics/          # Analytics center pages
│   │   ├── dashboard/          # Protected dashboard area
│   │   │   ├── layout.tsx      # Dashboard layout
│   │   │   ├── page.tsx        # Main dashboard
│   │   │   ├── analytics/      # Dashboard analytics
│   │   │   ├── detection/      # Disease detection tools
│   │   │   ├── health/         # Crop health monitoring
│   │   │   ├── marketplace/    # Marketplace integration
│   │   │   ├── recommend/      # Crop recommendations
│   │   │   └── settings/       # User settings
│   │   ├── detection/          # Standalone detection
│   │   ├── marketplace/        # Public marketplace
│   │   ├── recommend/          # Public recommendations
│   │   ├── sign-in/           # Authentication pages
│   │   ├── sign-up/           # User registration
│   │   └── api/               # API routes and middleware
│   ├── components/             # Reusable UI components
│   │   ├── ui/                # Radix UI base components
│   │   ├── CropRecommendationForm.tsx
│   │   ├── DashboardLayout.tsx
│   │   ├── DiseaseDetection.tsx
│   │   ├── Features.tsx
│   │   ├── Footer.tsx
│   │   ├── Header.tsx
│   │   └── Hero.tsx
│   ├── hooks/                 # Custom React hooks
│   │   └── use-mobile.ts      # Mobile device detection
│   ├── lib/                   # Utility libraries
│   │   ├── analytics.ts       # Analytics utilities
│   │   ├── api.ts            # API client configuration
│   │   ├── diseaseApi.ts     # Disease detection API
│   │   ├── marketplace.ts    # Marketplace API
│   │   └── utils.ts          # General utilities
│   └── middleware.ts          # Clerk auth middleware
├── public/                    # Static assets
│   ├── next.svg              # Next.js logo
│   ├── vercel.svg            # Vercel logo
│   └── *.svg                 # Additional icons
├── package.json              # Dependencies and scripts
├── next.config.ts            # Next.js configuration
├── tailwind.config.js        # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
├── postcss.config.mjs       # PostCSS configuration
├── components.json          # Radix UI component config
├── .env.local              # Environment variables
└── eslint.config.mjs       # ESLint configuration
```

## 🎨 **Design System**

### **Component Architecture**
- **Radix UI Primitives** - Accessible, unstyled base components
- **Custom UI Library** - Styled components in `/components/ui/`
- **Compound Components** - Complex features like forms and dashboards
- **Responsive Design** - Mobile-first approach with Tailwind breakpoints

### **Color Palette**
```css
/* Primary Agricultural Theme */
--green-50: #f0fdf4;
--green-600: #16a34a;
--green-700: #15803d;

/* Semantic Colors */
--success: #22c55e;
--warning: #eab308;
--error: #ef4444;
--info: #3b82f6;
```

### **Typography**
- **Geist Sans** - Primary font for body text
- **Geist Mono** - Monospace font for code and data
- **Responsive Scaling** - Adaptive font sizes across devices

### **Animation & Interactions**
- **Framer Motion** - Smooth page transitions (planned)
- **Tailwind Animations** - Utility-based micro-interactions
- **Loading States** - Skeleton screens and spinners

## 🚀 **Getting Started**

### **📋 Prerequisites**
- **Node.js** 18+ (LTS recommended)
- **npm**, **yarn**, **pnpm**, or **bun** package manager
- **Git** for version control
- **Modern Browser** (Chrome, Firefox, Safari, Edge)

### **⚡ Quick Setup**

#### **1. Install Dependencies**
```bash
cd client

# Using npm
npm install

# Using yarn
yarn install

# Using pnpm
pnpm install

# Using bun
bun install
```

#### **2. Environment Configuration**
Create `.env.local` file in the client directory:

```env
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_key
CLERK_SECRET_KEY=sk_test_your_clerk_secret

# API Endpoints
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
NEXT_PUBLIC_AI_API_URL=http://localhost:8000
NEXT_PUBLIC_DISEASE_API_URL=http://localhost:1234

# Application Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_SITE_NAME="CropAI"
NEXT_PUBLIC_SITE_DESCRIPTION="Smart Crop Disease Detection & Management"

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_MARKETPLACE=true
NEXT_PUBLIC_ENABLE_RECOMMENDATIONS=true

# Development
NODE_ENV=development
```

#### **3. Clerk Authentication Setup**
1. **Create Clerk Account** at [clerk.dev](https://clerk.dev)
2. **Create New Application** in Clerk dashboard
3. **Copy API Keys** to `.env.local`
4. **Configure Sign-in Methods** (Email, Social providers)
5. **Set Redirect URLs**:
   - Sign-in: `http://localhost:3000/dashboard`
   - Sign-up: `http://localhost:3000/dashboard`
   - Sign-out: `http://localhost:3000`

### **🏃‍♂️ Development Server**

#### **Start Next.js Application**
```bash
# Development with Turbopack (fastest)
npm run dev

# Alternative package managers
yarn dev
pnpm dev
bun dev
```

#### **Full Stack Development**
```bash
# Start all services (Frontend + AI Backend)
npm run dev-full

# Manually start backend services
npm run start-ai  # Starts AI v2 backend
```

#### **Access Application**
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:3000/api (if API routes exist)

### **🔧 Available Scripts**

```bash
# Development
npm run dev              # Start development server with Turbopack
npm run dev-full         # Start frontend + AI backend concurrently

# Production
npm run build            # Build production application with Turbopack
npm run start            # Start production server

# Code Quality
npm run lint             # Run ESLint for code analysis

# Backend Integration
npm run start-ai         # Start AI v2 backend server
```

### **🏗️ Build & Deployment**

#### **Production Build**
```bash
# Build optimized application
npm run build

# Start production server
npm run start
```

#### **Build Output**
```
.next/
├── static/             # Static assets with cache headers
├── server/             # Server-side code and pages
└── build/              # Client-side JavaScript bundles
```

#### **Environment-Specific Builds**
```bash
# Development build (with source maps)
NODE_ENV=development npm run build

# Production build (optimized)
NODE_ENV=production npm run build
```

## 🛠️ **Development Workflow**

### **🔄 Hot Reload & Fast Refresh**
- **Instant Updates** - Code changes reflect immediately
- **State Preservation** - React state maintained during updates
- **Error Overlay** - In-browser error messages with stack traces
- **Turbopack Speed** - Ultra-fast bundling and compilation

### **📱 Multi-Device Testing**
```bash
# Local network access
npm run dev -- --hostname 0.0.0.0

# Access from other devices
http://YOUR_LOCAL_IP:3000
```

### **🧪 Component Development**
```tsx
// Example component with Tailwind and TypeScript
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Leaf } from "lucide-react";

interface CropCardProps {
  name: string;
  health: number;
  diseaseRisk: 'low' | 'medium' | 'high';
}

export function CropCard({ name, health, diseaseRisk }: CropCardProps) {
  return (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center gap-3">
        <Leaf className="w-8 h-8 text-green-600" />
        <div>
          <h3 className="font-semibold text-lg">{name}</h3>
          <p className="text-gray-600">Health: {health}%</p>
          <Badge variant={diseaseRisk === 'low' ? 'success' : 'warning'}>
            {diseaseRisk} risk
          </Badge>
        </div>
      </div>
    </Card>
  );
}
```

### **🔗 API Integration**
```tsx
// Example API integration with error handling
import { api } from "@/lib/api";

export async function getCropRecommendations(farmData: FarmData) {
  try {
    const response = await api.post('/predict', farmData);
    return response.data;
  } catch (error) {
    console.error('Failed to get recommendations:', error);
    throw new Error('Recommendation service unavailable');
  }
}

// Usage in component
const [recommendations, setRecommendations] = useState([]);
const [loading, setLoading] = useState(false);

const handleGetRecommendations = async () => {
  setLoading(true);
  try {
    const data = await getCropRecommendations(farmData);
    setRecommendations(data.predictions);
  } catch (error) {
    toast.error('Failed to load recommendations');
  } finally {
    setLoading(false);
  }
};
```

### **🎨 Styling Guidelines**

#### **Tailwind CSS Usage**
```tsx
// Responsive design patterns
<div className="
  grid 
  grid-cols-1 
  md:grid-cols-2 
  lg:grid-cols-3 
  gap-6 
  p-4 
  md:p-8
">

// Color system
<Button className="
  bg-green-600 
  hover:bg-green-700 
  text-white 
  font-semibold
">

// Spacing and typography
<h1 className="
  text-3xl 
  md:text-4xl 
  lg:text-5xl 
  font-bold 
  text-gray-900 
  mb-6
">
```

#### **Component Variants**
```tsx
// Using class-variance-authority for component variants
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium",
  {
    variants: {
      variant: {
        default: "bg-green-600 text-white hover:bg-green-700",
        outline: "border border-green-600 text-green-600 hover:bg-green-50",
        ghost: "text-green-600 hover:bg-green-50"
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4",
        lg: "h-12 px-6 text-lg"
      }
    },
    defaultVariants: {
      variant: "default",
      size: "md"
    }
  }
);
```

## 🔌 **API Integration**

### **Backend Services Connection**
```typescript
// lib/api.ts - Centralized API configuration
const API_ENDPOINTS = {
  marketplace: process.env.NEXT_PUBLIC_API_BASE_URL, // Express.js server
  analytics: process.env.NEXT_PUBLIC_AI_API_URL,     // FastAPI server
  disease: process.env.NEXT_PUBLIC_DISEASE_API_URL   // Disease detection
};

// Disease detection API
export async function detectDisease(imageFile: File) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch(`${API_ENDPOINTS.disease}/predict`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
}

// Crop recommendations API
export async function getCropPrediction(farmData: any) {
  const response = await fetch(`${API_ENDPOINTS.analytics}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(farmData)
  });
  
  return response.json();
}
```

### **Error Handling & Loading States**
```tsx
// Custom hook for API calls with loading states
export function useApiCall<T>(apiFunction: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const execute = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiFunction();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };
  
  return { data, loading, error, execute };
}
```

## 📊 **Performance & Optimization**

### **Next.js 15 Features**
- **Turbopack** - 700x faster than Webpack for local development
- **App Router** - Improved routing with layouts and loading states
- **Server Components** - Reduced client-side JavaScript
- **Image Optimization** - Automatic WebP/AVIF conversion
- **Font Optimization** - Self-hosted Google Fonts

### **Bundle Analysis**
```bash
# Analyze bundle size
npx @next/bundle-analyzer
```

### **Performance Best Practices**
- **Code Splitting** - Automatic route-based splitting
- **Dynamic Imports** - Lazy load components
- **Image Optimization** - Next.js Image component
- **Font Loading** - Optimized Google Fonts
- **Caching** - Appropriate cache headers

## 🧪 **Testing Strategy**

### **Testing Tools** (Planned)
```bash
# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom jest

# Run tests
npm run test
```

### **Testing Examples**
```tsx
// Component testing example
import { render, screen } from '@testing-library/react';
import { CropCard } from '@/components/CropCard';

test('renders crop card with correct information', () => {
  render(
    <CropCard 
      name="Wheat" 
      health={85} 
      diseaseRisk="low" 
    />
  );
  
  expect(screen.getByText('Wheat')).toBeInTheDocument();
  expect(screen.getByText('Health: 85%')).toBeInTheDocument();
  expect(screen.getByText('low risk')).toBeInTheDocument();
});
```

## 🚀 **Deployment Options**

### **🌐 Vercel Deployment** (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to Vercel
vercel

# Production deployment
vercel --prod
```

#### **Vercel Configuration**
```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "env": {
    "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY": "@clerk_publishable_key",
    "CLERK_SECRET_KEY": "@clerk_secret_key"
  }
}
```

### **🐳 Docker Deployment**
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

```bash
# Build and run Docker container
docker build -t cropai-client .
docker run -p 3000:3000 cropai-client
```

### **☁️ Cloud Deployment Options**

#### **Netlify**
```bash
# Build command
npm run build

# Publish directory
.next
```

#### **AWS Amplify**
```yaml
# amplify.yml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
```

### **🔧 Environment Variables for Production**
```env
# Production environment variables
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_your_live_key
CLERK_SECRET_KEY=sk_live_your_live_secret
NEXT_PUBLIC_API_BASE_URL=https://api.cropai.com
NEXT_PUBLIC_AI_API_URL=https://ai.cropai.com
NEXT_PUBLIC_DISEASE_API_URL=https://disease.cropai.com
NEXT_PUBLIC_APP_URL=https://cropai.com
NODE_ENV=production
```

## 🔒 **Security & Best Practices**

### **Authentication Security**
- **Clerk Integration** - Industry-standard authentication
- **Route Protection** - Middleware-based access control
- **Session Management** - Secure token handling
- **CSRF Protection** - Built-in Next.js protection

### **Environment Security**
```bash
# Secure environment variable handling
NEXT_PUBLIC_* # Client-side variables (public)
CLERK_SECRET_KEY # Server-side only (private)
```

### **Code Security**
- **TypeScript** - Type safety prevents runtime errors
- **ESLint Rules** - Security-focused linting
- **Dependency Scanning** - Regular security updates
- **HTTPS Enforcement** - Production SSL requirements

## 📈 **Performance Metrics**

### **Core Web Vitals Targets**
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms  
- **CLS** (Cumulative Layout Shift): < 0.1
- **TTFB** (Time to First Byte): < 800ms

### **Bundle Size Optimization**
- **Tree Shaking** - Remove unused code
- **Code Splitting** - Route-based chunks
- **Dynamic Imports** - Lazy load features
- **Image Optimization** - WebP/AVIF formats

### **Monitoring & Analytics**
```tsx
// Google Analytics integration example
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
      <GoogleAnalytics gaId="GA_MEASUREMENT_ID" />
    </html>
  )
}
```

## 🔄 **Current Status & Roadmap**

### **✅ Completed Features**
- **Next.js 15 Setup** - Modern React framework with App Router
- **Authentication System** - Clerk integration with protected routes
- **Responsive Design** - Mobile-first UI with Tailwind CSS
- **Component Library** - Radix UI primitives with custom styling
- **Dashboard Structure** - Multi-page dashboard layout
- **Landing Page** - Marketing site with feature showcase
- **API Integration** - Backend service connections prepared
- **TypeScript Setup** - Full type safety implementation

### **🚧 In Development**
- **Disease Detection UI** - Image upload and analysis interface
- **Analytics Dashboard** - Data visualization with Recharts
- **Marketplace Interface** - Product browsing and purchasing
- **Real-time Updates** - WebSocket integration for live data
- **Mobile App Integration** - API synchronization with React Native app
- **Advanced Search** - Elasticsearch-powered product discovery

### **🎯 Future Enhancements**
- **Progressive Web App** - Offline functionality and push notifications
- **Advanced Analytics** - Custom dashboards and reporting
- **Multi-language Support** - Internationalization (i18n)
- **Dark Mode** - Theme switching capability
- **Performance Monitoring** - Real-time performance tracking
- **A/B Testing** - Feature experimentation framework
- **Advanced Security** - Two-factor authentication
- **Accessibility** - WCAG 2.1 AA compliance

### **📊 Performance Goals**
- **Load Time**: < 2 seconds on 3G networks
- **Bundle Size**: < 500KB initial JavaScript
- **SEO Score**: 95+ Lighthouse score
- **Accessibility**: 100% WCAG compliance

## 🛠️ **Troubleshooting**

### **Common Issues**

#### **Clerk Authentication Problems**
```bash
# Check environment variables
echo $NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
echo $CLERK_SECRET_KEY

# Verify Clerk configuration
npm run dev -- --debug
```

#### **Build Failures**
```bash
# Clear Next.js cache
rm -rf .next

# Clear node modules
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npx tsc --noEmit
```

#### **API Connection Issues**
```typescript
// Check API endpoints are accessible
const healthCheck = async () => {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/health`);
    console.log('API Status:', response.status);
  } catch (error) {
    console.error('API Connection Failed:', error);
  }
};
```

### **Development Tips**
- **Use Turbopack** - Significantly faster than Webpack
- **Check Browser Console** - Monitor for JavaScript errors
- **Verify Environment Variables** - Ensure all required vars are set
- **Test API Endpoints** - Use browser dev tools or Postman
- **Monitor Network Requests** - Check for failed API calls

## 📚 **Resources & Documentation**

### **Framework Documentation**
- **[Next.js 15](https://nextjs.org/docs)** - Framework documentation
- **[React 19](https://react.dev/)** - React documentation
- **[TypeScript](https://www.typescriptlang.org/docs/)** - TypeScript handbook

### **UI & Styling**
- **[Tailwind CSS](https://tailwindcss.com/docs)** - Utility-first CSS framework
- **[Radix UI](https://www.radix-ui.com/)** - Unstyled UI primitives
- **[Lucide React](https://lucide.dev/)** - Icon library

### **Authentication & Security**
- **[Clerk Documentation](https://clerk.dev/docs)** - Authentication solution
- **[Next.js Security](https://nextjs.org/docs/advanced-features/security-headers)** - Security best practices

### **Development Tools**
- **[Turbopack](https://turbo.build/pack)** - Next-generation bundler
- **[ESLint](https://eslint.org/)** - Code quality tool
- **[Vercel](https://vercel.com/docs)** - Deployment platform

## 📞 **Support & Information**

### **Project Details**
- **Repository**: hackbhoomi2025/client
- **Version**: 0.1.0
- **License**: Private
- **Framework**: Next.js 15.5.2
- **Language**: TypeScript 5

### **Development Environment**
- **Local URL**: http://localhost:3000
- **API Endpoint**: http://localhost:5000
- **AI Endpoint**: http://localhost:8000
- **Disease API**: http://localhost:1234

### **Production Environment**
- **Domain**: TBD (To Be Determined)
- **CDN**: Vercel Edge Network
- **Analytics**: Google Analytics (planned)
- **Monitoring**: Vercel Analytics (planned)

---

## 🌟 **Getting Help**

For development questions or issues:
1. **Check Documentation** - Review relevant framework docs
2. **Search Issues** - Look for similar problems in repository
3. **Check Environment** - Verify all prerequisites are met
4. **Test API Connections** - Ensure backend services are running
5. **Review Logs** - Check browser console and terminal output

**Happy Farming with AI! 🌾🤖**
