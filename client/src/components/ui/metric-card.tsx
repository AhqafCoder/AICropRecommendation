import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent } from "./card"

interface MetricCardProps {
  title: string
  value: string | number
  subtitle?: string
  icon?: React.ReactNode
  trend?: "up" | "down" | "neutral"
  trendValue?: string
  className?: string
  variant?: "default" | "success" | "warning" | "danger" | "info"
}

const MetricCard = React.forwardRef<HTMLDivElement, MetricCardProps>(
  ({ 
    title, 
    value, 
    subtitle, 
    icon, 
    trend, 
    trendValue, 
    className, 
    variant = "default" 
  }, ref) => {
    const variants = {
      default: "border-gray-200 bg-white",
      success: "border-green-200 bg-gradient-to-br from-green-50 to-emerald-50",
      warning: "border-yellow-200 bg-gradient-to-br from-yellow-50 to-orange-50", 
      danger: "border-red-200 bg-gradient-to-br from-red-50 to-pink-50",
      info: "border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50"
    }

    const iconColors = {
      default: "text-gray-600",
      success: "text-green-600",
      warning: "text-yellow-600",
      danger: "text-red-600", 
      info: "text-blue-600"
    }

    const trendColors = {
      up: "text-green-600",
      down: "text-red-600",
      neutral: "text-gray-500"
    }

    return (
      <Card 
        ref={ref} 
        className={cn(
          "border-2 hover:shadow-md transition-all duration-200",
          variants[variant],
          className
        )}
      >
        <CardContent className="p-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                {icon && (
                  <div className={cn("text-lg", iconColors[variant])}>
                    {icon}
                  </div>
                )}
                <h3 className="text-sm font-medium text-gray-600">{title}</h3>
              </div>
              
              <div className="space-y-1">
                <div className="text-2xl font-bold text-gray-900">
                  {value}
                </div>
                
                {subtitle && (
                  <div className="text-sm text-gray-500">
                    {subtitle}
                  </div>
                )}
                
                {trend && trendValue && (
                  <div className={cn("text-xs font-medium", trendColors[trend])}>
                    {trend === "up" ? "↗" : trend === "down" ? "↘" : "→"} {trendValue}
                  </div>
                )}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)
MetricCard.displayName = "MetricCard"

export { MetricCard }