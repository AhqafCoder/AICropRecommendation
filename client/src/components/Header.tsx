"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Leaf, 
  Menu, 
  X, 
  ChevronDown,
  Brain,
  Camera,
  BarChart3,
  ShoppingCart,
  User
} from "lucide-react";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigationItems = [
    { 
      name: "Recommend", 
      href: "/recommend",
      icon: Brain
    },
    { 
      name: "Detection", 
      href: "/detection",
      icon: Camera
    },
    { 
      name: "Analytics", 
      href: "/analytics",
      icon: BarChart3
    },
    { 
      name: "Marketplace", 
      href: "/marketplace",
      icon: ShoppingCart
    }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-b border-green-100 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
              <Leaf className="w-6 h-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-gray-900">CropAI</span>
              <Badge className="text-xs bg-green-100 text-green-800 px-1 py-0">
                Smart Farming
              </Badge>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigationItems.map((item) => {
              const IconComponent = item.icon;
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className="flex items-center space-x-1 text-gray-600 hover:text-green-600 transition-colors duration-200 font-medium"
                >
                  <IconComponent className="w-4 h-4" />
                  <span>{item.name}</span>
                </a>
              );
            })}
          </nav>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center space-x-4">
            <Button variant="ghost" className="text-gray-600 hover:text-green-600">
              <User className="w-4 h-4 mr-2" />
              Sign In
            </Button>
            <Button className="bg-green-600 hover:bg-green-700 text-white">
              Get Started
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600"
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-white border-t border-green-100">
              {navigationItems.map((item) => {
                const IconComponent = item.icon;
                return (
                  <a
                    key={item.name}
                    href={item.href}
                    className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-md transition-colors duration-200"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <IconComponent className="w-4 h-4" />
                    <span className="font-medium">{item.name}</span>
                  </a>
                );
              })}
              <div className="flex flex-col space-y-2 px-3 pt-4 border-t border-green-100 mt-4">
                <Button variant="ghost" className="justify-start text-gray-600 hover:text-green-600">
                  <User className="w-4 h-4 mr-2" />
                  Sign In
                </Button>
                <Button className="bg-green-600 hover:bg-green-700 text-white">
                  Get Started
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
