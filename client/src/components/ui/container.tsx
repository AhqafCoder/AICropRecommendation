import * as React from "react"
import { cn } from "@/lib/utils"

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "fluid" | "constrained"
}

const Container = React.forwardRef<HTMLDivElement, ContainerProps>(
  ({ className, variant = "default", ...props }, ref) => {
    const variants = {
      default: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
      fluid: "w-full px-4 sm:px-6 lg:px-8",
      constrained: "max-w-5xl mx-auto px-4 sm:px-6 lg:px-8"
    }

    return (
      <div
        ref={ref}
        className={cn(variants[variant], className)}
        {...props}
      />
    )
  }
)
Container.displayName = "Container"

export { Container }