import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart3, Camera, Leaf, ShoppingCart, Heart, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react"
import Link from "next/link"

const quickStats = [
  {
    title: "Crops Monitored",
    value: "24",
    change: "+12%",
    icon: Leaf,
    color: "text-green-600",
  },
  {
    title: "Disease Detections",
    value: "8",
    change: "-25%",
    icon: Camera,
    color: "text-blue-600",
  },
  {
    title: "Farm Health Score",
    value: "87%",
    change: "+5%",
    icon: Heart,
    color: "text-red-500",
  },
  {
    title: "Market Revenue",
    value: "₹45,230",
    change: "+18%",
    icon: ShoppingCart,
    color: "text-purple-600",
  },
]

const recentActivities = [
  {
    type: "success",
    message: "Tomato crop health improved by 15%",
    time: "2 hours ago",
    icon: CheckCircle,
  },
  {
    type: "warning",
    message: "Early blight detected in Field A",
    time: "4 hours ago", 
    icon: AlertTriangle,
  },
  {
    type: "info",
    message: "New fertilizer recommendation available",
    time: "6 hours ago",
    icon: TrendingUp,
  },
]

const quickActions = [
  {
    title: "Scan for Diseases",
    description: "Upload crop images for AI-powered disease detection",
    href: "/dashboard/detection",
    icon: Camera,
    color: "bg-blue-500 hover:bg-blue-600",
  },
  {
    title: "Get Crop Recommendations",
    description: "Receive personalized crop recommendations",
    href: "/dashboard/recommend",
    icon: Leaf,
    color: "bg-green-500 hover:bg-green-600",
  },
  {
    title: "View Analytics",
    description: "Analyze your farm performance metrics",
    href: "/dashboard/analytics",
    icon: BarChart3,
    color: "bg-purple-500 hover:bg-purple-600",
  },
  {
    title: "Browse Marketplace",
    description: "Buy seeds, fertilizers, and equipment",
    href: "/dashboard/marketplace",
    icon: ShoppingCart,
    color: "bg-orange-500 hover:bg-orange-600",
  },
]

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Welcome back, Farmer!</h1>
          <p className="text-gray-600 mt-1">Here&apos;s what&apos;s happening with your farm today.</p>
        </div>
        <Button asChild>
          <Link href="/dashboard/detection">
            <Camera className="mr-2 h-4 w-4" />
            Quick Scan
          </Link>
        </Button>
      </div>

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {quickStats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                <span className={stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}>
                  {stat.change}
                </span>
                {' '}from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Frequently used tools and features</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            {quickActions.map((action) => (
              <Button
                key={action.title}
                asChild
                variant="outline"
                className="h-auto p-4 justify-start"
              >
                <Link href={action.href}>
                  <div className={`p-2 rounded-md mr-3 ${action.color}`}>
                    <action.icon className="h-4 w-4 text-white" />
                  </div>
                  <div className="text-left">
                    <div className="font-medium">{action.title}</div>
                    <div className="text-sm text-gray-500">{action.description}</div>
                  </div>
                </Link>
              </Button>
            ))}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest updates from your farm</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className={`mt-0.5 p-1 rounded-full ${
                    activity.type === 'success' ? 'bg-green-100 text-green-600' :
                    activity.type === 'warning' ? 'bg-yellow-100 text-yellow-600' :
                    'bg-blue-100 text-blue-600'
                  }`}>
                    <activity.icon className="h-3 w-3" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Farm Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Farm Overview</CardTitle>
          <CardDescription>Key insights about your agricultural operations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <Leaf className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <h3 className="font-semibold text-green-800">Healthy Crops</h3>
              <p className="text-2xl font-bold text-green-600">18/24</p>
              <p className="text-sm text-green-600">75% of crops are healthy</p>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <Camera className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <h3 className="font-semibold text-blue-800">AI Scans Today</h3>
              <p className="text-2xl font-bold text-blue-600">12</p>
              <p className="text-sm text-blue-600">Disease detection scans</p>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <BarChart3 className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <h3 className="font-semibold text-purple-800">Yield Prediction</h3>
              <p className="text-2xl font-bold text-purple-600">+12%</p>
              <p className="text-sm text-purple-600">Expected increase</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}