import { DashboardLayout } from "@/components/DashboardLayout"

export default function DashboardRootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <DashboardLayout>{children}</DashboardLayout>
}