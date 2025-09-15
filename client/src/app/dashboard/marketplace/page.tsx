import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ShoppingCart, Star, Package, Truck, Leaf, Droplets, Zap } from "lucide-react"

const featuredProducts = [
  {
    id: 1,
    name: "Organic Tomato Seeds",
    price: "₹450",
    originalPrice: "₹600",
    rating: 4.8,
    reviews: 124,
    image: "/api/placeholder/200/200",
    category: "Seeds",
    seller: "Green Valley Seeds",
    discount: "25% OFF",
    description: "High-yield organic tomato seeds resistant to common diseases",
  },
  {
    id: 2,
    name: "Bio-Fertilizer NPK 20:20:20",
    price: "₹890",
    originalPrice: "₹1,200",
    rating: 4.6,
    reviews: 89,
    image: "/api/placeholder/200/200",
    category: "Fertilizers",
    seller: "AgriCare Solutions",
    discount: "26% OFF",
    description: "Complete nutrition for all crops with slow-release formula",
  },
  {
    id: 3,
    name: "Smart Irrigation Controller",
    price: "₹12,500",
    originalPrice: "₹15,000",
    rating: 4.9,
    reviews: 45,
    image: "/api/placeholder/200/200",
    category: "Equipment",
    seller: "FarmTech India",
    discount: "17% OFF",
    description: "WiFi-enabled automatic irrigation system with weather integration",
  },
  {
    id: 4,
    name: "Organic Pesticide Spray",
    price: "₹320",
    originalPrice: "₹400",
    rating: 4.7,
    reviews: 203,
    image: "/api/placeholder/200/200",
    category: "Pesticides",
    seller: "EcoGarden Products",
    discount: "20% OFF",
    description: "Natural pest control solution safe for organic farming",
  },
]

const categories = [
  { name: "Seeds & Saplings", icon: Leaf, count: "200+ products", color: "bg-green-100 text-green-700" },
  { name: "Fertilizers", icon: Droplets, count: "150+ products", color: "bg-blue-100 text-blue-700" },
  { name: "Farm Equipment", icon: Zap, count: "80+ products", color: "bg-purple-100 text-purple-700" },
  { name: "Pesticides", icon: Package, count: "120+ products", color: "bg-yellow-100 text-yellow-700" },
]

export default function MarketplacePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Marketplace</h1>
          <p className="text-gray-600 mt-1">Find quality seeds, fertilizers, and equipment for your farm</p>
        </div>
        <Button>
          <ShoppingCart className="mr-2 h-4 w-4" />
          View Cart (3)
        </Button>
      </div>

      

      {/* Featured Products */}
      
        
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {featuredProducts.map((product) => (
              <Card key={product.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                <div className="aspect-square bg-gray-100 relative">
                  <div className="absolute top-2 left-2">
                    <Badge variant="destructive">{product.discount}</Badge>
                  </div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Package className="h-16 w-16 text-gray-300" />
                  </div>
                </div>
                <CardContent className="p-4">
                  <div className="space-y-2">
                    <h3 className="font-semibold text-sm">{product.name}</h3>
                    <p className="text-xs text-gray-600 line-clamp-2">{product.description}</p>
                    <div className="flex items-center space-x-1">
                      <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                      <span className="text-xs">{product.rating}</span>
                      <span className="text-xs text-gray-500">({product.reviews})</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-green-600">{product.price}</span>
                      <span className="text-xs text-gray-500 line-through">{product.originalPrice}</span>
                    </div>
                    <p className="text-xs text-gray-600">by {product.seller}</p>
                    <Button size="sm" className="w-full">
                      <ShoppingCart className="mr-1 h-3 w-3" />
                      Add to Cart
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Truck className="h-8 w-8 text-blue-600" />
              <div>
                <h3 className="font-semibold">Free Delivery</h3>
                <p className="text-sm text-gray-600">On orders above ₹1,000</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Star className="h-8 w-8 text-yellow-500" />
              <div>
                <h3 className="font-semibold">Quality Assured</h3>
                <p className="text-sm text-gray-600">100% genuine products</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Package className="h-8 w-8 text-green-600" />
              <div>
                <h3 className="font-semibold">Easy Returns</h3>
                <p className="text-sm text-gray-600">15-day return policy</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}