import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Heart, AlertTriangle, CheckCircle, ThermometerSun, Droplets, Wind, Calendar } from "lucide-react"

const healthMetrics = [
  {
    title: "Overall Farm Health",
    score: 87,
    status: "Excellent",
    icon: Heart,
    color: "text-green-600",
    bgColor: "bg-green-100",
  },
  {
    title: "Soil Quality",
    score: 92,
    status: "Excellent",
    icon: CheckCircle,
    color: "text-green-600",
    bgColor: "bg-green-100",
  },
  {
    title: "Crop Vitality",
    score: 78,
    status: "Good",
    icon: CheckCircle,
    color: "text-yellow-600",
    bgColor: "bg-yellow-100",
  },
  {
    title: "Disease Risk",
    score: 15,
    status: "Low Risk",
    icon: AlertTriangle,
    color: "text-green-600",
    bgColor: "bg-green-100",
  },
]

const environmentalData = [
  {
    label: "Temperature",
    value: "28°C",
    status: "Optimal",
    icon: ThermometerSun,
    color: "text-green-600",
  },
  {
    label: "Humidity",
    value: "65%",
    status: "Good",
    icon: Droplets,
    color: "text-blue-600",
  },
  {
    label: "Wind Speed",
    value: "12 km/h",
    status: "Moderate",
    icon: Wind,
    color: "text-gray-600",
  },
  {
    label: "Last Rainfall",
    value: "3 days ago",
    status: "Recent",
    icon: Calendar,
    color: "text-blue-600",
  },
]

const cropStatus = [
  {
    name: "Tomato Field A",
    health: 95,
    status: "Excellent",
    lastCheck: "2 hours ago",
    issues: 0,
  },
  {
    name: "Wheat Field B",
    health: 78,
    status: "Good",
    lastCheck: "4 hours ago",
    issues: 1,
  },
  {
    name: "Corn Field C",
    health: 85,
    status: "Good",
    lastCheck: "1 hour ago",
    issues: 0,
  },
  {
    name: "Potato Field D",
    health: 92,
    status: "Excellent",
    lastCheck: "3 hours ago",
    issues: 0,
  },
]

const alerts = [
  {
    type: "warning",
    title: "Nutrient Deficiency Detected",
    description: "Wheat Field B showing signs of nitrogen deficiency",
    time: "2 hours ago",
    action: "Apply nitrogen-rich fertilizer",
  },
  {
    type: "info",
    title: "Irrigation Scheduled",
    description: "Automatic irrigation will start in 30 minutes",
    time: "30 minutes",
    action: "Monitor water levels",
  },
  {
    type: "success",
    title: "Pest Control Effective",
    description: "Aphid population reduced by 85% in Tomato Field A",
    time: "6 hours ago",
    action: "Continue monitoring",
  },
]

export default function HealthPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Farm Health Status</h1>
        <p className="text-gray-600 mt-1">Monitor the overall health and vitality of your crops and farm environment</p>
      </div>

      {/* Health Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {healthMetrics.map((metric) => (
          <Card key={metric.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
              <div className={`p-2 rounded-full ${metric.bgColor}`}>
                <metric.icon className={`h-4 w-4 ${metric.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.score}{metric.title === "Disease Risk" ? "%" : "/100"}</div>
              <div className="flex items-center space-x-2 mt-2">
                <Progress value={metric.title === "Disease Risk" ? 100 - metric.score : metric.score} className="flex-1" />
                <Badge variant={metric.status === "Excellent" ? "default" : "secondary"}>{metric.status}</Badge>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Environmental Conditions */}
        <Card>
          <CardHeader>
            <CardTitle>Environmental Conditions</CardTitle>
            <CardDescription>Current weather and environmental factors</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4">
              {environmentalData.map((data) => (
                <div key={data.label} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <data.icon className={`h-5 w-5 ${data.color}`} />
                    <div>
                      <h4 className="font-medium">{data.label}</h4>
                      <p className="text-sm text-gray-500">{data.status}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">{data.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Alerts & Notifications */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
            <CardDescription>Important notifications and recommendations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {alerts.map((alert, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 border rounded-lg">
                  <div className={`mt-0.5 p-1 rounded-full ${
                    alert.type === 'warning' ? 'bg-yellow-100 text-yellow-600' :
                    alert.type === 'info' ? 'bg-blue-100 text-blue-600' :
                    'bg-green-100 text-green-600'
                  }`}>
                    {alert.type === 'warning' ? <AlertTriangle className="h-3 w-3" /> :
                     alert.type === 'info' ? <Calendar className="h-3 w-3" /> :
                     <CheckCircle className="h-3 w-3" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-sm">{alert.title}</h4>
                    <p className="text-xs text-gray-600">{alert.description}</p>
                    <p className="text-xs text-gray-500 mt-1">Action: {alert.action}</p>
                    <p className="text-xs text-gray-400">{alert.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Individual Crop Status */}
      <Card>
        <CardHeader>
          <CardTitle>Individual Crop Health</CardTitle>
          <CardDescription>Detailed health status for each crop field</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            {cropStatus.map((crop) => (
              <div key={crop.name} className="p-4 border rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold">{crop.name}</h3>
                  <Badge variant={crop.status === "Excellent" ? "default" : "secondary"}>
                    {crop.status}
                  </Badge>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Health Score</span>
                    <span className="font-medium">{crop.health}/100</span>
                  </div>
                  <Progress value={crop.health} className="h-2" />
                  <div className="flex items-center justify-between text-xs text-gray-500">
                    <span>Last checked: {crop.lastCheck}</span>
                    <span>{crop.issues} issues detected</span>
                  </div>
                </div>
                <Button size="sm" variant="outline" className="w-full mt-3">
                  View Details
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Health Trends */}
      <Card>
        <CardHeader>
          <CardTitle>Health Trends</CardTitle>
          <CardDescription>Track health improvements over time</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center p-12 border-2 border-dashed border-gray-200 rounded-lg">
            <Heart className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="font-semibold text-gray-700 mb-2">Health Trend Charts</h3>
            <p className="text-sm text-gray-500">Interactive charts showing health trends over the past 6 months</p>
            <Button className="mt-4" variant="outline">View Detailed Analytics</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}