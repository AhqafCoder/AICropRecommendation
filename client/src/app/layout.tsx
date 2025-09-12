import { ClerkProvider } from '@clerk/nextjs';
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CropAI - Smart Crop Disease Detection & Management",
  description: "Advanced AI-powered crop disease detection and management system. Upload images of your crops to get instant disease diagnosis, treatment recommendations, and agricultural insights powered by machine learning.",
  keywords: [
    "crop disease detection",
    "agricultural AI",
    "plant disease diagnosis",
    "smart farming",
    "precision agriculture",
    "crop health monitoring",
    "AI agriculture",
    "plant pathology",
    "farming technology",
    "crop management"
  ],
  authors: [{ name: "CropAI Team" }],
  creator: "CropAI",
  publisher: "CropAI",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://cropai.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: "CropAI - Smart Crop Disease Detection & Management",
    description: "Advanced AI-powered crop disease detection and management system. Get instant disease diagnosis and treatment recommendations for your crops.",
    url: 'https://cropai.com',
    siteName: 'CropAI',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'CropAI - Smart Crop Disease Detection',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: "CropAI - Smart Crop Disease Detection & Management",
    description: "Advanced AI-powered crop disease detection and management system. Get instant disease diagnosis and treatment recommendations for your crops.",
    images: ['/twitter-image.png'],
    creator: '@cropai',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: [
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon.ico', sizes: 'any' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
    other: [
      { rel: 'android-chrome-192x192', url: '/android-chrome-192x192.png' },
      { rel: 'android-chrome-512x512', url: '/android-chrome-512x512.png' },
    ],
  },
  manifest: '/site.webmanifest',
  category: 'agriculture',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>{children}</body>
      </html>
    </ClerkProvider>
  );
}
