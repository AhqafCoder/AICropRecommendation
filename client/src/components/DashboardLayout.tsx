"use client";

import { Sidebar, SidebarContent, SidebarFooter, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarProvider, SidebarRail, SidebarTrigger } from "@/components/ui/sidebar"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { SignOutButton, useUser } from "@clerk/nextjs"
import { 
  Home, 
  BarChart3, 
  Camera, 
  Leaf, 
  ShoppingCart, 
  Heart, 
  Settings, 
  HelpCircle,
  LogOut,
  ChevronUp
} from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

const sidebarItems = [
  {
    title: "Dashboard",
    icon: Home,
    url: "/dashboard",
  },
  {
    title: "Analytics",
    icon: BarChart3,
    url: "/dashboard/analytics",
  },
  {
    title: "Disease Detection",
    icon: Camera,
    url: "/dashboard/detection",
  },
  {
    title: "Crop Recommendation",
    icon: Leaf,
    url: "/dashboard/recommend",
  },
  {
    title: "Marketplace",
    icon: ShoppingCart,
    url: "/dashboard/marketplace",
  },
  {
    title: "Farm Health",
    icon: Heart,
    url: "/dashboard/health",
  },
]

const supportItems = [
  {
    title: "Settings",
    icon: Settings,
    url: "/dashboard/settings",
  },
  {
    title: "Help & Support",
    icon: HelpCircle,
    url: "/dashboard/help",
  },
]

export function AppSidebar() {
  const { user } = useUser()
  const pathname = usePathname()

  return (
    <Sidebar variant="inset" className="border-r border-emerald-200 bg-gradient-to-b from-emerald-50 to-green-50">
      <SidebarHeader className="border-b border-emerald-200 bg-white/80">
        <div className="flex items-center gap-3 px-4 py-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-green-600 shadow-lg">
            <Leaf className="h-5 w-5 text-white" />
          </div>
          <div className="grid flex-1 text-left text-sm leading-tight">
            <span className="truncate font-bold text-emerald-800 text-lg">CropAI</span>
            <span className="truncate text-xs text-emerald-600">Smart Farming Platform</span>
          </div>
        </div>
      </SidebarHeader>
      
      <SidebarContent className="bg-gradient-to-b from-white to-emerald-50/50">
        <SidebarGroup>
          <SidebarGroupLabel className="text-emerald-700 font-semibold">Main Features</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sidebarItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    asChild 
                    isActive={pathname === item.url}
                    className="hover:bg-emerald-100 hover:text-emerald-800 data-[active=true]:bg-gradient-to-r data-[active=true]:from-emerald-500 data-[active=true]:to-green-600 data-[active=true]:text-white data-[active=true]:shadow-lg transition-all duration-200"
                  >
                    <Link href={item.url}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        
        <SidebarGroup>
          <SidebarGroupLabel className="text-emerald-700 font-semibold">Support</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {supportItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    asChild 
                    isActive={pathname === item.url}
                    className="hover:bg-emerald-100 hover:text-emerald-800 data-[active=true]:bg-gradient-to-r data-[active=true]:from-emerald-500 data-[active=true]:to-green-600 data-[active=true]:text-white data-[active=true]:shadow-lg transition-all duration-200"
                  >
                    <Link href={item.url}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      
      <SidebarFooter className="bg-white/80 border-t border-emerald-200">
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton
                  size="lg"
                  className="data-[state=open]:bg-emerald-100 data-[state=open]:text-emerald-800 hover:bg-emerald-50 border border-emerald-200"
                >
                  <Avatar className="h-8 w-8 rounded-lg border-2 border-emerald-300">
                    <AvatarImage src={user?.imageUrl} alt={user?.fullName || ''} />
                    <AvatarFallback className="rounded-lg bg-gradient-to-br from-emerald-500 to-green-600 text-white font-semibold">
                      {user?.firstName?.charAt(0) || 'U'}
                      {user?.lastName?.charAt(0) || ''}
                    </AvatarFallback>
                  </Avatar>
                  <div className="grid flex-1 text-left text-sm leading-tight">
                    <span className="truncate font-semibold text-emerald-800">{user?.fullName || 'User'}</span>
                    <span className="truncate text-xs text-emerald-600">{user?.primaryEmailAddress?.emailAddress}</span>
                  </div>
                  <ChevronUp className="ml-auto size-4 text-emerald-600" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg border-emerald-200"
                side="bottom"
                align="end"
                sideOffset={4}
              >
                <DropdownMenuItem asChild>
                  <Link href="/dashboard/settings" className="flex items-center">
                    <Settings className="mr-2 h-4 w-4 text-emerald-600" />
                    <span className="text-emerald-800">Account Settings</span>
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-emerald-200" />
                <DropdownMenuItem asChild>
                  <SignOutButton>
                    <div className="flex items-center cursor-pointer text-red-600 hover:text-red-800">
                      <LogOut className="mr-2 h-4 w-4" />
                      Sign out
                    </div>
                  </SignOutButton>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="flex-1 overflow-auto">
        <div className="flex h-16 items-center border-b border-gray-200 px-6">
          <SidebarTrigger className="mr-4" />
          <h1 className="text-lg font-semibold">Farm Dashboard</h1>
        </div>
        <div className="p-6">
          {children}
        </div>
      </main>
    </SidebarProvider>
  )
}