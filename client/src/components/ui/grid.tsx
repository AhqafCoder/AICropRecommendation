import * as React from "react"
import { cn } from "@/lib/utils"

interface GridProps extends React.HTMLAttributes<HTMLDivElement> {
  cols?: 1 | 2 | 3 | 4 | 5 | 6 | 12
  gap?: "sm" | "md" | "lg" | "xl"
  responsive?: boolean
}

const Grid = React.forwardRef<HTMLDivElement, GridProps>(
  ({ className, cols = 1, gap = "md", responsive = true, ...props }, ref) => {
    const gapClasses = {
      sm: "gap-2",
      md: "gap-4",
      lg: "gap-6", 
      xl: "gap-8"
    }

    const getGridCols = () => {
      if (!responsive) return `grid-cols-${cols}`
      
      switch (cols) {
        case 1: return "grid-cols-1"
        case 2: return "grid-cols-1 sm:grid-cols-2"
        case 3: return "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
        case 4: return "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4"
        case 5: return "grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5"
        case 6: return "grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6"
        case 12: return "grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 2xl:grid-cols-12"
        default: return "grid-cols-1"
      }
    }

    return (
      <div
        ref={ref}
        className={cn("grid", getGridCols(), gapClasses[gap], className)}
        {...props}
      />
    )
  }
)
Grid.displayName = "Grid"

export { Grid }