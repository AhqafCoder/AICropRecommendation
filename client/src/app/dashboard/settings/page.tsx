import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { UserProfile } from "@clerk/nextjs"
import { Bell, Shield, Globe, Database } from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Manage your account preferences and farm settings</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Quick Settings */}
        <div className="lg:col-span-1 space-y-6">
          {/* Notification Settings */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Notifications
              </CardTitle>
              <CardDescription>Configure your notification preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Disease Alerts</Label>
                  <p className="text-sm text-gray-500">Get notified when diseases are detected</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Weather Updates</Label>
                  <p className="text-sm text-gray-500">Receive weather alerts and forecasts</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Irrigation Reminders</Label>
                  <p className="text-sm text-gray-500">Reminders for irrigation schedules</p>
                </div>
                <Switch />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Market Updates</Label>
                  <p className="text-sm text-gray-500">Latest prices and market trends</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          {/* Farm Settings */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Farm Configuration
              </CardTitle>
              <CardDescription>Configure your farm details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="farm-size">Farm Size (acres)</Label>
                <Input id="farm-size" placeholder="Enter farm size" defaultValue="25" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="location">Location</Label>
                <Input id="location" placeholder="Enter location" defaultValue="Maharashtra, India" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="farming-type">Farming Type</Label>
                <Select defaultValue="organic">
                  <SelectTrigger>
                    <SelectValue placeholder="Select farming type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="organic">Organic</SelectItem>
                    <SelectItem value="conventional">Conventional</SelectItem>
                    <SelectItem value="mixed">Mixed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="primary-crop">Primary Crop</Label>
                <Select defaultValue="tomato">
                  <SelectTrigger>
                    <SelectValue placeholder="Select primary crop" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="tomato">Tomato</SelectItem>
                    <SelectItem value="wheat">Wheat</SelectItem>
                    <SelectItem value="rice">Rice</SelectItem>
                    <SelectItem value="corn">Corn</SelectItem>
                    <SelectItem value="potato">Potato</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Language & Region */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5" />
                Language & Region
              </CardTitle>
              <CardDescription>Set your language and regional preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="language">Language</Label>
                <Select defaultValue="en">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="hi">हिंदी (Hindi)</SelectItem>
                    <SelectItem value="mr">मराठी (Marathi)</SelectItem>
                    <SelectItem value="te">తెలుగు (Telugu)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="currency">Currency</Label>
                <Select defaultValue="inr">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="inr">₹ INR</SelectItem>
                    <SelectItem value="usd">$ USD</SelectItem>
                    <SelectItem value="eur">€ EUR</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="timezone">Timezone</Label>
                <Select defaultValue="ist">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ist">IST (India Standard Time)</SelectItem>
                    <SelectItem value="utc">UTC</SelectItem>
                    <SelectItem value="est">EST</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Profile Settings */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Profile Settings</CardTitle>
              <CardDescription>Manage your personal information and account security</CardDescription>
            </CardHeader>
            <CardContent>
              <UserProfile 
                appearance={{
                  elements: {
                    card: "shadow-none border-0",
                    navbar: "hidden",
                    pageScrollBox: "p-0",
                  }
                }}
              />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Data & Privacy */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Data & Privacy
          </CardTitle>
          <CardDescription>Control how your data is used and stored</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Data Analytics</Label>
                  <p className="text-sm text-gray-500">Allow us to analyze your farm data to improve recommendations</p>
                </div>
                <Switch defaultChecked />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Marketing Communications</Label>
                  <p className="text-sm text-gray-500">Receive emails about new features and products</p>
                </div>
                <Switch />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Research Participation</Label>
                  <p className="text-sm text-gray-500">Participate in agricultural research studies</p>
                </div>
                <Switch />
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Data Export</h4>
                <p className="text-sm text-gray-600 mb-3">Download a copy of your farm data</p>
                <Button variant="outline">Download Data</Button>
              </div>
              <Separator />
              <div>
                <h4 className="font-medium mb-2 text-red-600">Delete Account</h4>
                <p className="text-sm text-gray-600 mb-3">Permanently delete your account and all associated data</p>
                <Button variant="destructive">Delete Account</Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Changes */}
      <div className="flex justify-end space-x-2">
        <Button variant="outline">Cancel</Button>
        <Button>Save Changes</Button>
      </div>
    </div>
  )
}