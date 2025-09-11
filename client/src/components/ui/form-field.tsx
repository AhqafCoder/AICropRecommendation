import * as React from "react"
import { cn } from "@/lib/utils"
import { Label } from "./label"
import { Badge } from "./badge"

interface FormFieldProps {
  label: string
  icon?: React.ReactNode
  badge?: string
  badgeVariant?: "default" | "secondary" | "outline"
  error?: string
  hint?: string
  required?: boolean
  className?: string
  children: React.ReactNode
}

const FormField = React.forwardRef<HTMLDivElement, FormFieldProps>(
  ({ 
    label, 
    icon, 
    badge, 
    badgeVariant = "outline", 
    error, 
    hint, 
    required, 
    className, 
    children 
  }, ref) => {
    return (
      <div ref={ref} className={cn("space-y-2", className)}>
        <div className="flex items-center justify-between">
          <Label className={cn(
            "flex items-center gap-2 text-sm font-medium",
            error && "text-red-600"
          )}>
            {icon && <span className="text-base">{icon}</span>}
            {label}
            {required && <span className="text-red-500">*</span>}
          </Label>
          {badge && (
            <Badge variant={badgeVariant} className="text-xs font-semibold">
              {badge}
            </Badge>
          )}
        </div>
        
        <div className="relative">
          {children}
          {error && (
            <div className="absolute -bottom-6 left-0 text-xs text-red-600 font-medium">
              {error}
            </div>
          )}
        </div>
        
        {hint && !error && (
          <div className="text-xs text-gray-500 mt-1">
            {hint}
          </div>
        )}
      </div>
    )
  }
)
FormField.displayName = "FormField"

export { FormField }