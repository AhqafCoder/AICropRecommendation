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
    <Sidebar variant="inset" className="border-r border-gray-200">
      <SidebarHeader className="border-b border-gray-200">
        <div className="flex items-center gap-2 px-4 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-600">
            <Leaf className="h-4 w-4 text-white" />
          </div>
          <div className="grid flex-1 text-left text-sm leading-tight">
            <span className="truncate font-semibold">CropAI</span>
            <span className="truncate text-xs text-gray-500">Smart Farming Platform</span>
          </div>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Main Features</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {sidebarItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    asChild 
                    isActive={pathname === item.url}
                    className="hover:bg-green-50 hover:text-green-700 data-[active=true]:bg-green-100 data-[active=true]:text-green-800"
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
          <SidebarGroupLabel>Support</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {supportItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    asChild 
                    isActive={pathname === item.url}
                    className="hover:bg-green-50 hover:text-green-700 data-[active=true]:bg-green-100 data-[active=true]:text-green-800"
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
      
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton
                  size="lg"
                  className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                >
                  <Avatar className="h-8 w-8 rounded-lg">
                    <AvatarImage src={user?.imageUrl} alt={user?.fullName || ''} />
                    <AvatarFallback className="rounded-lg bg-green-100 text-green-700">
                      {user?.firstName?.charAt(0) || 'U'}
                      {user?.lastName?.charAt(0) || ''}
                    </AvatarFallback>
                  </Avatar>
                  <div className="grid flex-1 text-left text-sm leading-tight">
                    <span className="truncate font-semibold">{user?.fullName || 'User'}</span>
                    <span className="truncate text-xs text-gray-500">{user?.primaryEmailAddress?.emailAddress}</span>
                  </div>
                  <ChevronUp className="ml-auto size-4" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                side="bottom"
                align="end"
                sideOffset={4}
              >
                <DropdownMenuItem asChild>
                  <Link href="/dashboard/profile">
                    <Settings className="mr-2 h-4 w-4" />
                    Account Settings
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <SignOutButton>
                    <div className="flex items-center cursor-pointer">
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