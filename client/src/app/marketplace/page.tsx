"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { MarketplaceService, Product, MarketPrice } from "@/lib/marketplace";
import { 
  Search, 
  Filter, 
  Star, 
  MapPin, 
  Phone, 
  TrendingUp, 
  TrendingDown,
  Minus,
  ShoppingCart,
  Users,
  Package,
  DollarSign,
  Loader2
} from "lucide-react";

const sampleProducts: Product[] = [
  {
    id: '1',
    name: 'Premium Rice Seeds (IR64)',
    category: 'seeds',
    price: 120,
    unit: 'kg',
    seller: 'Green Valley Seeds',
    location: 'Punjab, India',
    rating: 4.8,
    reviews: 156,
    inStock: true,
    image: '🌾',
    description: 'High-yield IR64 rice variety suitable for kharif season',
    priceChange: -2.5
  },
  {
    id: '2',
    name: 'NPK Fertilizer (20:20:0)',
    category: 'fertilizer',
    price: 850,
    unit: '50kg bag',
    seller: 'FarmTech Solutions',
    location: 'Maharashtra, India',
    rating: 4.6,
    reviews: 89,
    inStock: true,
    image: '🌱',
    description: 'Balanced NPK fertilizer for optimal crop growth',
    priceChange: 3.2
  },
  {
    id: '3',
    name: 'Solar Water Pump',
    category: 'equipment',
    price: 45000,
    unit: 'unit',
    seller: 'AgriTech India',
    location: 'Gujarat, India',
    rating: 4.9,
    reviews: 34,
    inStock: true,
    image: '⚡',
    description: '5HP solar-powered water pump with 2-year warranty',
    priceChange: -1.8
  },
  {
    id: '4',
    name: 'Organic Pesticide',
    category: 'pesticide',
    price: 320,
    unit: 'liter',
    seller: 'Bio Solutions',
    location: 'Karnataka, India',
    rating: 4.7,
    reviews: 78,
    inStock: false,
    image: '🛡️',
    description: 'Eco-friendly organic pesticide for crop protection',
    priceChange: 0.5
  }
];

const marketPrices: MarketPrice[] = [
  {
    crop: 'Rice',
    currentPrice: 2100,
    unit: 'quintal',
    change: 50,
    changePercent: 2.4,
    market: 'Delhi Mandi',
    lastUpdated: '2 hours ago'
  },
  {
    crop: 'Wheat',
    currentPrice: 2050,
    unit: 'quintal',
    change: -30,
    changePercent: -1.4,
    market: 'Punjab Mandi',
    lastUpdated: '1 hour ago'
  },
  {
    crop: 'Cotton',
    currentPrice: 5800,
    unit: 'quintal',
    change: 120,
    changePercent: 2.1,
    market: 'Gujarat Mandi',
    lastUpdated: '3 hours ago'
  },
  {
    crop: 'Sugarcane',
    currentPrice: 320,
    unit: 'quintal',
    change: 0,
    changePercent: 0,
    market: 'UP Mandi',
    lastUpdated: '4 hours ago'
  }
];

export default function MarketplacePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [marketPrices, setMarketPrices] = useState<MarketPrice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadMarketplaceData();
  }, []);

  const loadMarketplaceData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [productsData, pricesData] = await Promise.all([
        MarketplaceService.getProducts(),
        MarketplaceService.getMarketPrices()
      ]);

      setProducts(productsData);
      setMarketPrices(pricesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load marketplace data');
      console.error('Error loading marketplace data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    try {
      setLoading(true);
      const filters = {
        search: searchQuery,
        category: selectedCategory === 'all' ? undefined : selectedCategory
      };
      const filteredProducts = await MarketplaceService.getProducts(filters);
      setProducts(filteredProducts);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const categories = [
    { id: 'all', name: 'All Products', icon: Package },
    { id: 'seeds', name: 'Seeds', icon: '🌾' },
    { id: 'fertilizer', name: 'Fertilizers', icon: '🌱' },
    { id: 'equipment', name: 'Equipment', icon: '⚙️' },
    { id: 'pesticide', name: 'Pesticides', icon: '🛡️' }
  ];

  const filteredProducts = products.filter(product => {
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.seller.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  if (loading && products.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <Header />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
            <p>Loading marketplace...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <Header />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <p className="text-red-600 mb-4">Error: {error}</p>
            <Button onClick={loadMarketplaceData}>Try Again</Button>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', { 
      style: 'currency', 
      currency: 'INR' 
    }).format(amount);
  };

  const getPriceChangeIcon = (change: number) => {
    if (change > 0) return <TrendingUp className="w-4 h-4 text-green-600" />;
    if (change < 0) return <TrendingDown className="w-4 h-4 text-red-600" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getPriceChangeColor = (change: number) => {
    if (change > 0) return 'text-green-600';
    if (change < 0) return 'text-red-600';
    return 'text-gray-400';
  };

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-white pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Agricultural Marketplace
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Connect with verified suppliers, compare prices, and get the best deals on agricultural products
          </p>
        </div>

        {/* Market Insights Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-green-600" />
              Live Market Prices
            </CardTitle>
            <CardDescription>
              Real-time crop prices from major mandis across India
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {marketPrices.map((price, index) => (
                <div key={index} className="p-4 border rounded-lg bg-white">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">{price.crop}</h3>
                    <div className="flex items-center gap-1">
                      {getPriceChangeIcon(price.change)}
                      <span className={`text-sm font-medium ${getPriceChangeColor(price.change)}`}>
                        {price.changePercent > 0 ? '+' : ''}{price.changePercent}%
                      </span>
                    </div>
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">
                    {formatCurrency(price.currentPrice)}
                  </div>
                  <div className="text-sm text-gray-500">
                    per {price.unit}
                  </div>
                  <div className="text-xs text-gray-400 mt-2">
                    {price.market} • {price.lastUpdated}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="flex-1 relative flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                type="text"
                placeholder="Search products, sellers..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="pl-10"
              />
            </div>
            <Button onClick={handleSearch} disabled={loading}>
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Search'}
            </Button>
          </div>
          <div className="flex gap-2 overflow-x-auto">
            {categories.map((category) => (
              <Button
                key={category.id}
                variant={selectedCategory === category.id ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  setSelectedCategory(category.id);
                  // Trigger search after category change
                  setTimeout(handleSearch, 100);
                }}
                className="whitespace-nowrap"
              >
                {typeof category.icon === 'string' ? (
                  <span className="mr-2">{category.icon}</span>
                ) : (
                  <category.icon className="w-4 h-4 mr-2" />
                )}
                {category.name}
              </Button>
            ))}
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <ShoppingCart className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Products</p>
                  <p className="text-2xl font-bold text-gray-900">2,847</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Verified Sellers</p>
                  <p className="text-2xl font-bold text-gray-900">456</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Package className="w-6 h-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Orders This Month</p>
                  <p className="text-2xl font-bold text-gray-900">1,238</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <DollarSign className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Avg. Savings</p>
                  <p className="text-2xl font-bold text-gray-900">15%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map((product) => (
            <Card key={product.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              <CardContent className="p-0">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="text-4xl">{product.image}</div>
                    <div className="text-right">
                      <div className="flex items-center gap-1">
                        {getPriceChangeIcon(product.priceChange)}
                        <span className={`text-sm ${getPriceChangeColor(product.priceChange)}`}>
                          {product.priceChange > 0 ? '+' : ''}{product.priceChange}%
                        </span>
                      </div>
                      {!product.inStock && (
                        <Badge variant="destructive" className="mt-1">Out of Stock</Badge>
                      )}
                    </div>
                  </div>

                  <h3 className="font-semibold text-lg text-gray-900 mb-2">
                    {product.name}
                  </h3>
                  
                  <p className="text-gray-600 text-sm mb-4">
                    {product.description}
                  </p>

                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      <span className="text-sm font-medium">{product.rating}</span>
                    </div>
                    <span className="text-sm text-gray-500">
                      ({product.reviews} reviews)
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mb-4">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-sm text-gray-600">{product.location}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xl font-bold text-gray-900">
                        {formatCurrency(product.price)}
                      </span>
                      <span className="text-sm text-gray-500 ml-1">
                        per {product.unit}
                      </span>
                    </div>
                    <Button 
                      size="sm" 
                      disabled={!product.inStock}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      {product.inStock ? 'Add to Cart' : 'Out of Stock'}
                    </Button>
                  </div>

                  <div className="mt-3 pt-3 border-t">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">
                        {product.seller}
                      </span>
                      <Button variant="outline" size="sm">
                        <Phone className="w-4 h-4 mr-1" />
                        Contact
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No products found</h3>
            <p className="text-gray-500">Try adjusting your search or filter criteria</p>
          </div>
        )}
      </div>
    </div>
      <Footer />
    </>
  );
}
