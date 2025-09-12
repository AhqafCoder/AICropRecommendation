import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart3, TrendingUp, Leaf, DollarSign, Calendar, AlertCircle } from "lucide-react"

const analyticsData = [
  {
    title: "Crop Yield Trends",
    description: "Monthly yield analysis across all crops",
    value: "2,340 kg",
    change: "+12.5%",
    icon: BarChart3,
    period: "This month",
  },
  {
    title: "Revenue Growth", 
    description: "Total revenue from crop sales",
    value: "₹1,25,670",
    change: "+18.2%",
    icon: DollarSign,
    period: "Last 30 days",
  },
  {
    title: "Healthy Crops",
    description: "Percentage of crops in good health",
    value: "87.5%",
    change: "+5.1%",
    icon: Leaf,
    period: "Current status",
  },
  {
    title: "Disease Incidents",
    description: "Number of disease cases detected",
    value: "8 cases",
    change: "-23.4%",
    icon: AlertCircle,
    period: "This month",
  },
]

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Farm Analytics</h1>
        <p className="text-gray-600 mt-1">Comprehensive insights into your farm performance and trends</p>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {analyticsData.map((metric) => (
          <Card key={metric.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
              <metric.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value}</div>
              <p className="text-xs text-muted-foreground">
                <span className={metric.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}>
                  {metric.change}
                </span>
                {' '}{metric.period}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Crop Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Crop Performance Overview</CardTitle>
            <CardDescription>Health status and yield data for all crops</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { crop: "Tomatoes", health: 92, yield: "High", status: "Excellent" },
                { crop: "Wheat", health: 78, yield: "Medium", status: "Good" },
                { crop: "Corn", health: 85, yield: "High", status: "Good" },
                { crop: "Potatoes", health: 95, yield: "Very High", status: "Excellent" },
              ].map((crop) => (
                <div key={crop.crop} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <h4 className="font-medium">{crop.crop}</h4>
                    <p className="text-sm text-gray-500">Health: {crop.health}% | Yield: {crop.yield}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    crop.status === 'Excellent' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {crop.status}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Insights */}
        <Card>
          <CardHeader>
            <CardTitle>AI Insights & Recommendations</CardTitle>
            <CardDescription>Smart recommendations based on your farm data</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  type: "recommendation",
                  title: "Optimal Planting Time",
                  description: "Consider planting summer crops in the next 2 weeks for maximum yield",
                  icon: Calendar,
                },
                {
                  type: "warning",
                  title: "Weather Alert",
                  description: "Heavy rainfall predicted next week. Prepare drainage systems",
                  icon: AlertCircle,
                },
                {
                  type: "success",
                  title: "Yield Improvement",
                  description: "Your potato yield increased by 15% compared to last season",
                  icon: TrendingUp,
                },
              ].map((insight, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 border rounded-lg">
                  <div className={`mt-0.5 p-2 rounded-full ${
                    insight.type === 'recommendation' ? 'bg-blue-100 text-blue-600' :
                    insight.type === 'warning' ? 'bg-yellow-100 text-yellow-600' :
                    'bg-green-100 text-green-600'
                  }`}>
                    <insight.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="font-medium">{insight.title}</h4>
                    <p className="text-sm text-gray-600">{insight.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Charts Section */}
      <Card>
        <CardHeader>
          <CardTitle>Historical Trends</CardTitle>
          <CardDescription>6-month overview of key farm metrics</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="text-center p-8 border-2 border-dashed border-gray-200 rounded-lg">
              <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
              <h3 className="font-semibold text-gray-700">Yield Trends Chart</h3>
              <p className="text-sm text-gray-500">Interactive chart showing monthly yield data</p>
            </div>
            <div className="text-center p-8 border-2 border-dashed border-gray-200 rounded-lg">
              <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-2" />
              <h3 className="font-semibold text-gray-700">Revenue Analytics</h3>
              <p className="text-sm text-gray-500">Revenue trends and profit analysis</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}