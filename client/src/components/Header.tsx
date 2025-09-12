"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { SignInButton, SignUpButton, UserButton, useUser } from "@clerk/nextjs";
import Link from "next/link";
import { 
  Leaf, 
  Menu, 
  X, 
  Brain,
  Camera,
  BarChart3,
  ShoppingCart
} from "lucide-react";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { isSignedIn } = useUser();

  const navigationItems = [
    { 
      name: "Recommend", 
      href: "/dashboard/recommend",
      icon: Brain
    },
    { 
      name: "Detection", 
      href: "/dashboard/detection",
      icon: Camera
    },
    { 
      name: "Analytics", 
      href: "/dashboard/analytics",
      icon: BarChart3
    },
    { 
      name: "Marketplace", 
      href: "/dashboard/marketplace",
      icon: ShoppingCart
    }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-b border-green-100 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <Link href={isSignedIn ? "/dashboard" : "/"} className="flex items-center space-x-2">
              <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
                <Leaf className="w-6 h-6 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                  CropAI
                </h1>
                <p className="text-xs text-gray-500 -mt-1">Smart Farming</p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg text-gray-700 hover:text-green-600 hover:bg-green-50 transition-colors"
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* Auth Buttons / User Menu */}
          <div className="flex items-center space-x-3">
            {isSignedIn ? (
              <div className="flex items-center space-x-3">
                <Link href="/dashboard">
                  <Button variant="outline" size="sm">
                    Dashboard
                  </Button>
                </Link>
                <UserButton 
                  appearance={{
                    elements: {
                      avatarBox: "w-8 h-8"
                    }
                  }}
                />
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <SignInButton mode="modal">
                  <Button variant="outline" size="sm">
                    Sign In
                  </Button>
                </SignInButton>
                <SignUpButton mode="modal">
                  <Button size="sm" className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600">
                    Get Started
                  </Button>
                </SignUpButton>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 rounded-lg text-gray-700 hover:text-green-600 hover:bg-green-50"
            >
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <nav className="flex flex-col space-y-2">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-700 hover:text-green-600 hover:bg-green-50 transition-colors"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                );
              })}
              {!isSignedIn && (
                <div className="pt-4 border-t border-gray-100 space-y-2">
                  <SignInButton mode="modal">
                    <Button variant="outline" className="w-full">
                      Sign In
                    </Button>
                  </SignInButton>
                  <SignUpButton mode="modal">
                    <Button className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600">
                      Get Started
                    </Button>
                  </SignUpButton>
                </div>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}
