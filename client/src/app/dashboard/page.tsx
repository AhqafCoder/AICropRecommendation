"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart3, Camera, Leaf, ShoppingCart, Heart, TrendingUp, AlertTriangle, CheckCircle, DollarSign } from "lucide-react"
import { useUser } from "@clerk/nextjs"
import Link from "next/link"
import { useEffect, useState } from "react"

interface DashboardStats {
  cropsMonitored: number
  diseaseDetections: number
  farmHealthScore: number
  marketRevenue: number
  totalUsers: number
  monthlyGrowth: number
}

interface Activity {
  type: "success" | "warning" | "info"
  message: string
  time: string
  icon: React.ComponentType<{ className?: string }>
}

const quickActions = [
  {
    title: "AI Disease Scanner",
    description: "Upload crop images for instant AI-powered disease detection",
    href: "/dashboard/detection",
    icon: Camera,
    gradient: "from-emerald-500 to-green-600",
  },
  {
    title: "Smart Crop Advisor",
    description: "Get personalized crop recommendations based on soil conditions",
    href: "/dashboard/recommend",
    icon: Leaf,
    gradient: "from-green-500 to-emerald-600",
  },
  {
    title: "Farm Analytics Hub",
    description: "Analyze performance metrics and optimize your farming strategy",
    href: "/dashboard/analytics",
    icon: BarChart3,
    gradient: "from-green-600 to-emerald-700",
  },
  {
    title: "CropAI Marketplace",
    description: "Source premium seeds, fertilizers, and farming equipment",
    href: "/dashboard/marketplace",
    icon: ShoppingCart,
    gradient: "from-emerald-600 to-green-700",
  },
]

export default function DashboardPage() {
  const { user } = useUser()
  const [stats, setStats] = useState<DashboardStats>({
    cropsMonitored: 0,
    diseaseDetections: 0,
    farmHealthScore: 0,
    marketRevenue: 0,
    totalUsers: 0,
    monthlyGrowth: 0
  })
  const [activities, setActivities] = useState<Activity[]>([])
  const [loading, setLoading] = useState(true)

  const userName = user?.firstName || user?.fullName || "Farmer"

  useEffect(() => {
    // Fetch dashboard data from backend
    const fetchDashboardData = async () => {
      try {
        // Call Express.js backend
        const statsResponse = await fetch('http://localhost:5000/api/dashboard/stats')
        const statsData = await statsResponse.json()
        
        if (statsData.success) {
          setStats({
            cropsMonitored: 2340,
            diseaseDetections: 12,
            farmHealthScore: 87.5,
            marketRevenue: 1256670,
            totalUsers: 1247,
            monthlyGrowth: 18.2
          })
        } else {
          // Fallback data
          setStats({
            cropsMonitored: 24 + Math.floor(Math.random() * 10),
            diseaseDetections: 8 - Math.floor(Math.random() * 3),
            farmHealthScore: 85 + Math.floor(Math.random() * 10),
            marketRevenue: 45230 + Math.floor(Math.random() * 5000),
            totalUsers: 1247,
            monthlyGrowth: 12 + Math.floor(Math.random() * 8)
          })
        }

        setActivities([
          {
            type: "success",
            message: `${userName}'s tomato crop health improved by 15%`,
            time: "2 hours ago",
            icon: CheckCircle,
          },
          {
            type: "warning",
            message: "Early blight detected in Field A - treatment recommended",
            time: "4 hours ago", 
            icon: AlertTriangle,
          },
          {
            type: "info",
            message: "New organic fertilizer recommendation available",
            time: "6 hours ago",
            icon: TrendingUp,
          },
        ])
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        // Use default fallback values on error
        setStats({
          cropsMonitored: 24,
          diseaseDetections: 8,
          farmHealthScore: 85,
          marketRevenue: 45230,
          totalUsers: 1247,
          monthlyGrowth: 12
        })
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [userName])

  const quickStatsData = [
    {
      title: "Crops Monitored",
      value: stats.cropsMonitored.toString(),
      change: "+12%",
      icon: Leaf,
      color: "text-emerald-600",
      bgColor: "bg-emerald-50",
      borderColor: "border-emerald-200",
    },
    {
      title: "Disease Detections",
      value: stats.diseaseDetections.toString(),
      change: "-25%",
      icon: Camera,
      color: "text-green-600",
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
    },
    {
      title: "Farm Health Score",
      value: `${stats.farmHealthScore}%`,
      change: "+5%",
      icon: Heart,
      color: "text-emerald-700",
      bgColor: "bg-emerald-50",
      borderColor: "border-emerald-200",
    },
    {
      title: "Market Revenue",
      value: `₹${stats.marketRevenue.toLocaleString()}`,
      change: `+${stats.monthlyGrowth}%`,
      icon: DollarSign,
      color: "text-green-700",
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
    },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your CropAI dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-4 sm:p-6">
      {/* Welcome Section with CropAI Branding */}
      <div className="bg-gradient-to-br from-emerald-50 to-green-100 rounded-2xl p-6 sm:p-8 border border-emerald-200">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl flex items-center justify-center">
                <Leaf className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-emerald-700 to-green-800 bg-clip-text text-transparent">
                  Welcome back, {userName}!
                </h1>
                <p className="text-emerald-700/80 text-sm sm:text-base">CropAI Smart Farming Platform</p>
              </div>
            </div>
            <p className="text-emerald-600 text-sm sm:text-base">Here&apos;s what&apos;s happening with your farm today.</p>
          </div>
          <Button asChild size="lg" className="bg-gradient-to-r from-emerald-600 to-green-700 hover:from-emerald-700 hover:to-green-800 text-white shadow-lg">
            <Link href="/dashboard/detection" className="flex items-center gap-2">
              <Camera className="w-5 h-5" />
              <span className="hidden sm:inline">Quick AI Scan</span>
              <span className="sm:hidden">Scan Now</span>
            </Link>
          </Button>
        </div>
      </div>

      {/* Quick Stats with Enhanced Green Theme */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        {quickStatsData.map((stat) => (
          <Card key={stat.title} className={`${stat.bgColor} ${stat.borderColor} border-2 hover:shadow-lg transition-all duration-200`}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium text-gray-700">{stat.title}</CardTitle>
              <div className={`p-2 rounded-lg ${stat.bgColor} ${stat.borderColor} border`}>
                <stat.icon className={`h-3 w-3 sm:h-4 sm:w-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-xl sm:text-2xl font-bold text-gray-900">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                <span className={stat.change.startsWith('+') ? 'text-emerald-600 font-medium' : 'text-red-600 font-medium'}>
                  {stat.change}
                </span>
                {' '}from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Quick Actions with Enhanced Design */}
        <Card className="border-emerald-200 bg-gradient-to-br from-white to-emerald-50">
          <CardHeader>
            <CardTitle className="text-emerald-800 flex items-center gap-2">
              <div className="w-6 h-6 bg-emerald-600 rounded-lg flex items-center justify-center">
                <Leaf className="w-4 h-4 text-white" />
              </div>
              CropAI Quick Actions
            </CardTitle>
            <CardDescription>AI-powered tools for modern farming</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            {quickActions.map((action) => (
              <Button
                key={action.title}
                asChild
                variant="outline"
                className="h-auto p-4 justify-start border-emerald-200 hover:bg-emerald-50 hover:border-emerald-300 transition-all duration-200"
              >
                <Link href={action.href}>
                  <div className={`p-3 rounded-xl mr-4 bg-gradient-to-br ${action.gradient} shadow-lg`}>
                    <action.icon className="h-5 w-5 text-white" />
                  </div>
                  <div className="text-left flex-1">
                    <div className="font-semibold text-gray-900 text-sm sm:text-base">{action.title}</div>
                    <div className="text-xs sm:text-sm text-gray-600 mt-1">{action.description}</div>
                  </div>
                </Link>
              </Button>
            ))}
          </CardContent>
        </Card>

        {/* Recent Activity with Green Theme */}
        <Card className="border-emerald-200 bg-gradient-to-br from-white to-green-50">
          <CardHeader>
            <CardTitle className="text-green-800 flex items-center gap-2">
              <div className="w-6 h-6 bg-green-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-4 h-4 text-white" />
              </div>
              Farm Activity Feed
            </CardTitle>
            <CardDescription>Latest updates from your CropAI system</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {activities.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 rounded-lg bg-white/60 border border-emerald-100">
                  <div className={`mt-0.5 p-2 rounded-full ${
                    activity.type === 'success' ? 'bg-emerald-100 text-emerald-600' :
                    activity.type === 'warning' ? 'bg-yellow-100 text-yellow-600' :
                    'bg-green-100 text-green-600'
                  }`}>
                    <activity.icon className="h-4 w-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900 font-medium">{activity.message}</p>
                    <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Farm Overview with CropAI Branding */}
      <Card className="border-emerald-200 bg-gradient-to-br from-emerald-50 to-green-50">
        <CardHeader>
          <CardTitle className="text-emerald-800 flex items-center gap-2">
            <div className="w-6 h-6 bg-gradient-to-br from-emerald-500 to-green-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-4 h-4 text-white" />
            </div>
            CropAI Farm Intelligence
          </CardTitle>
          <CardDescription>AI-powered insights for optimal farm management</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div className="text-center p-6 bg-white rounded-xl border-2 border-emerald-200 shadow-sm">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl flex items-center justify-center mx-auto mb-3">
                <Leaf className="h-6 w-6 text-white" />
              </div>
              <h3 className="font-semibold text-emerald-800 mb-1">Healthy Crops</h3>
              <p className="text-2xl font-bold text-emerald-600">{Math.floor(stats.cropsMonitored * 0.75)}/{stats.cropsMonitored}</p>
              <p className="text-sm text-emerald-600">AI Health Score: {stats.farmHealthScore}%</p>
            </div>
            <div className="text-center p-6 bg-white rounded-xl border-2 border-green-200 shadow-sm">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center mx-auto mb-3">
                <Camera className="h-6 w-6 text-white" />
              </div>
              <h3 className="font-semibold text-green-800 mb-1">AI Scans Today</h3>
              <p className="text-2xl font-bold text-green-600">{12 + Math.floor(Math.random() * 8)}</p>
              <p className="text-sm text-green-600">Disease detection active</p>
            </div>
            <div className="text-center p-6 bg-white rounded-xl border-2 border-emerald-200 shadow-sm sm:col-span-2 lg:col-span-1">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-600 to-green-700 rounded-xl flex items-center justify-center mx-auto mb-3">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <h3 className="font-semibold text-emerald-800 mb-1">Yield Prediction</h3>
              <p className="text-2xl font-bold text-emerald-600">+{stats.monthlyGrowth}%</p>
              <p className="text-sm text-emerald-600">AI-predicted increase</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}