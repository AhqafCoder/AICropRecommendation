import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const skeletonVariants = cva(
  "animate-pulse rounded-md bg-muted",
  {
    variants: {
      variant: {
        default: "bg-slate-100 dark:bg-slate-800",
        shimmer: "bg-gradient-to-r from-slate-100 via-slate-200 to-slate-100 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Skeleton({
  className,
  variant,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof skeletonVariants>) {
  return (
    <div
      className={cn(skeletonVariants({ variant, className }))}
      {...props}
    />
  )
}

export { Skeleton }