import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { 
  Card, 
  Title, 
  Chip, 
  Surface,
  Button,
  Searchbar,
  Badge
} from 'react-native-paper';
import { 
  ShoppingBag, 
  Package, 
  Truck, 
  Star,
  Filter,
  Heart,
  Plus,
  Leaf,
  Beaker,
  Wrench,
  Droplets
} from 'lucide-react-native';

export default function ShopScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = [
    { id: 'all', label: 'All', icon: ShoppingBag },
    { id: 'fertilizers', label: 'Fertilizers', icon: Beaker },
    { id: 'seeds', label: 'Seeds', icon: Leaf },
    { id: 'tools', label: 'Tools', icon: Wrench },
    { id: 'irrigation', label: 'Irrigation', icon: Droplets }
  ];

  const featuredProducts = [
    { 
      id: 1, 
      name: 'Organic Fertilizer Premium', 
      price: '$25.99', 
      originalPrice: '$32.99',
      rating: 4.8,
      reviews: 124,
      category: 'fertilizers',
      badge: 'BESTSELLER',
      discount: '22% OFF',
      image: '🌱',
      inStock: true
    },
    { 
      id: 2, 
      name: 'Heirloom Tomato Seeds', 
      price: '$12.50', 
      originalPrice: null,
      rating: 4.9,
      reviews: 89,
      category: 'seeds',
      badge: 'NEW',
      discount: null,
      image: '🍅',
      inStock: true
    },
    { 
      id: 3, 
      name: 'Bio-Pesticide Spray', 
      price: '$18.75', 
      originalPrice: '$22.00',
      rating: 4.6,
      reviews: 156,
      category: 'fertilizers',
      badge: 'ECO-FRIENDLY',
      discount: '15% OFF',
      image: '🌿',
      inStock: false
    },
    { 
      id: 4, 
      name: 'Professional Garden Tool Set', 
      price: '$45.00', 
      originalPrice: '$55.00',
      rating: 4.7,
      reviews: 203,
      category: 'tools',
      badge: 'PREMIUM',
      discount: '18% OFF',
      image: '🔧',
      inStock: true
    },
    { 
      id: 5, 
      name: 'Drip Irrigation Kit', 
      price: '$89.99', 
      originalPrice: '$110.00',
      rating: 4.5,
      reviews: 67,
      category: 'irrigation',
      badge: 'WATER-SAVER',
      discount: '18% OFF',
      image: '💧',
      inStock: true
    },
    { 
      id: 6, 
      name: 'Cucumber Seeds Pack', 
      price: '$8.99', 
      originalPrice: null,
      rating: 4.7,
      reviews: 45,
      category: 'seeds',
      badge: null,
      discount: null,
      image: '🥒',
      inStock: true
    }
  ];

  const getBadgeColor = (badge: string | null) => {
    switch (badge) {
      case 'BESTSELLER': return '#ef4444';
      case 'NEW': return '#22c55e';
      case 'ECO-FRIENDLY': return '#84cc16';
      case 'PREMIUM': return '#8b5cf6';
      case 'WATER-SAVER': return '#06b6d4';
      default: return '#6b7280';
    }
  };

  const filteredProducts = selectedCategory === 'all' 
    ? featuredProducts 
    : featuredProducts.filter(product => product.category === selectedCategory);

  return (
    <View className="flex-1 bg-gray-50">
      <StatusBar barStyle="light-content" backgroundColor="#16a34a" />
      
      {/* Header */}
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="pt-12 pb-6 px-5"
      >
        <View className="flex-row items-center justify-between mb-4">
          <View>
            <Text className="text-2xl font-bold text-white mb-1">🛒 AgriShop</Text>
            <Text className="text-white/90">Quality agricultural products</Text>
          </View>
          <View className="flex-row space-x-2">
            <TouchableOpacity className="bg-white/20 rounded-full p-2">
              <Heart size={24} color="#fff" />
            </TouchableOpacity>
            <TouchableOpacity className="bg-white/20 rounded-full p-2 relative">
              <ShoppingBag size={24} color="#fff" />
              <Badge className="absolute -top-1 -right-1 bg-red-500" size={18}>3</Badge>
            </TouchableOpacity>
          </View>
        </View>
      </LinearGradient>

      <ScrollView 
        className="flex-1" 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        {/* Search Bar */}
        <View className="px-4 py-4">
          <Searchbar
            placeholder="Search products..."
            onChangeText={setSearchQuery}
            value={searchQuery}
            style={{ backgroundColor: '#fff', elevation: 2 }}
            iconColor="#22c55e"
          />
        </View>

        {/* Categories */}
        <View className="px-4 mb-6">
          <ScrollView horizontal showsHorizontalScrollIndicator={false} className="space-x-3">
            {categories.map((category) => (
              <TouchableOpacity
                key={category.id}
                onPress={() => setSelectedCategory(category.id)}
                className={`mr-3 ${category.id === 'irrigation' ? 'mr-0' : ''}`}
              >
                <Surface
                  className={`px-4 py-3 rounded-full flex-row items-center ${
                    selectedCategory === category.id ? 'bg-green-600' : 'bg-white'
                  }`}
                  elevation={selectedCategory === category.id ? 3 : 1}
                >
                  <category.icon 
                    size={18} 
                    color={selectedCategory === category.id ? '#fff' : '#22c55e'} 
                  />
                  <Text 
                    className={`ml-2 font-medium ${
                      selectedCategory === category.id ? 'text-white' : 'text-gray-800'
                    }`}
                  >
                    {category.label}
                  </Text>
                </Surface>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Delivery Info Banner */}
        <Card className="mx-4 mb-6 bg-gradient-to-r from-blue-50 to-green-50" elevation={2}>
          <Card.Content className="p-4">
            <View className="flex-row items-center">
              <View className="bg-green-100 rounded-full p-2 mr-3">
                <Truck size={24} color="#22c55e" />
              </View>
              <View className="flex-1">
                <Text className="text-gray-800 font-semibold">Free Delivery</Text>
                <Text className="text-gray-600 text-sm">On orders above $50 • Express delivery available</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Featured Products */}
        <View className="px-4">
          <Text className="text-xl font-bold text-gray-800 mb-4">
            {selectedCategory === 'all' ? 'Featured Products' : `${categories.find(c => c.id === selectedCategory)?.label}`}
          </Text>
          
          <View className="flex-row flex-wrap justify-between">
            {filteredProducts.map((product) => (
              <Card key={product.id} className="w-[48%] mb-4 bg-white" elevation={3}>
                <Card.Content className="p-4">
                  {/* Product Badge */}
                  {product.badge && (
                    <View className="absolute top-2 left-2 z-10">
                      <Chip 
                        className="h-6"
                        textStyle={{ 
                          fontSize: 10, 
                          fontWeight: '600',
                          color: '#fff'
                        }}
                        style={{ backgroundColor: getBadgeColor(product.badge) }}
                      >
                        {product.badge}
                      </Chip>
                    </View>
                  )}

                  {/* Discount Badge */}
                  {product.discount && (
                    <View className="absolute top-2 right-2 z-10">
                      <Chip 
                        className="h-6 bg-red-500"
                        textStyle={{ 
                          fontSize: 10, 
                          fontWeight: '600',
                          color: '#fff'
                        }}
                      >
                        {product.discount}
                      </Chip>
                    </View>
                  )}

                  {/* Product Image */}
                  <View className="items-center py-6 mb-3">
                    <Text className="text-4xl">{product.image}</Text>
                  </View>

                  {/* Product Info */}
                  <Text className="text-gray-800 font-semibold text-sm mb-2 leading-5">
                    {product.name}
                  </Text>

                  {/* Rating */}
                  <View className="flex-row items-center mb-3">
                    <Star size={14} color="#fbbf24" fill="#fbbf24" />
                    <Text className="text-gray-600 text-xs ml-1">
                      {product.rating} ({product.reviews})
                    </Text>
                  </View>

                  {/* Price */}
                  <View className="flex-row items-center justify-between mb-3">
                    <View>
                      <Text className="text-green-600 font-bold text-lg">{product.price}</Text>
                      {product.originalPrice && (
                        <Text className="text-gray-400 text-sm line-through">
                          {product.originalPrice}
                        </Text>
                      )}
                    </View>
                    <View className={`px-2 py-1 rounded-full ${product.inStock ? 'bg-green-100' : 'bg-red-100'}`}>
                      <Text className={`text-xs font-medium ${product.inStock ? 'text-green-700' : 'text-red-700'}`}>
                        {product.inStock ? 'In Stock' : 'Out of Stock'}
                      </Text>
                    </View>
                  </View>

                  {/* Add to Cart Button */}
                  <Button
                    mode="contained"
                    onPress={() => {}}
                    disabled={!product.inStock}
                    className={product.inStock ? 'bg-green-600' : 'bg-gray-400'}
                    contentStyle={{ paddingVertical: 4 }}
                    labelStyle={{ fontSize: 12, fontWeight: '600' }}
                    icon={() => <Plus size={16} color="#fff" />}
                  >
                    {product.inStock ? 'Add to Cart' : 'Out of Stock'}
                  </Button>
                </Card.Content>
              </Card>
            ))}
          </View>
        </View>

        {/* Load More Button */}
        <View className="px-4 mt-4">
          <Button
            mode="outlined"
            onPress={() => {}}
            className="border-green-600"
            contentStyle={{ paddingVertical: 8 }}
            labelStyle={{ color: '#22c55e', fontSize: 16, fontWeight: '600' }}
          >
            Load More Products
          </Button>
        </View>
      </ScrollView>
    </View>
  );
}
