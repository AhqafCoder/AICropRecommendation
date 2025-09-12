import * as React from "react"
import { cn } from "@/lib/utils"

interface SectionProps extends React.HTMLAttributes<HTMLElement> {
  variant?: "default" | "hero" | "feature" | "cta"
  spacing?: "sm" | "md" | "lg" | "xl"
}

const Section = React.forwardRef<HTMLElement, SectionProps>(
  ({ className, variant = "default", spacing = "lg", ...props }, ref) => {
    const variants = {
      default: "bg-white",
      hero: "bg-gradient-to-br from-green-50 via-blue-50 to-purple-50",
      feature: "bg-gray-50/50",
      cta: "bg-gradient-to-r from-green-600 to-emerald-600 text-white"
    }

    const spacingClasses = {
      sm: "py-8",
      md: "py-12", 
      lg: "py-16",
      xl: "py-24"
    }

    return (
      <section
        ref={ref}
        className={cn(variants[variant], spacingClasses[spacing], className)}
        {...props}
      />
    )
  }
)
Section.displayName = "Section"

export { Section }