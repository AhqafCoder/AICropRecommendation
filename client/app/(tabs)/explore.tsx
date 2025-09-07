import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StatusBar } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { 
  Card, 
  Title, 
  Chip, 
  Surface,
  Searchbar,
  Avatar,
  Button
} from 'react-native-paper';
import { 
  Search, 
  BookOpen, 
  Video, 
  Users, 
  Award, 
  Leaf,
  TrendingUp,
  Clock,
  Play,
  MessageCircle,
  Heart,
  Share
} from 'lucide-react-native';

export default function ExploreScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTab, setSelectedTab] = useState('resources');

  const learningResources = [
    { 
      id: 1, 
      title: 'Organic Farming Essentials', 
      type: 'Article', 
      duration: '5 min read',
      difficulty: 'Beginner',
      icon: BookOpen,
      thumbnail: '🌱',
      author: 'Dr. Sarah Green',
      views: '2.3K',
      rating: 4.8
    },
    { 
      id: 2, 
      title: 'Advanced Soil Testing Methods', 
      type: 'Video', 
      duration: '12 min',
      difficulty: 'Advanced',
      icon: Video,
      thumbnail: '🔬',
      author: 'Prof. Mike Johnson',
      views: '1.8K',
      rating: 4.9
    },
    { 
      id: 3, 
      title: 'Integrated Pest Management', 
      type: 'Course', 
      duration: '2h 30min',
      difficulty: 'Intermediate',
      icon: BookOpen,
      thumbnail: '🐛',
      author: 'AgriExpert Team',
      views: '890',
      rating: 4.7
    },
    { 
      id: 4, 
      title: 'Smart Irrigation Techniques', 
      type: 'Video', 
      duration: '15 min',
      difficulty: 'Intermediate',
      icon: Video,
      thumbnail: '💧',
      author: 'Emma Rodriguez',
      views: '3.1K',
      rating: 4.6
    }
  ];

  const communityPosts = [
    { 
      id: 1, 
      author: 'FarmerJoe', 
      avatar: 'FJ',
      time: '2h ago',
      content: 'Incredible harvest this season! The AI weather predictions helped me optimize watering schedules. Yield increased by 25% compared to last year! 🌾',
      likes: 47,
      comments: 12,
      shares: 8,
      tags: ['success', 'weather', 'yield']
    },
    { 
      id: 2, 
      author: 'GreenThumb', 
      avatar: 'GT',
      time: '4h ago',
      content: 'Has anyone tried the new bio-fertilizer from EcoGrow? Looking for honest reviews before making a bulk purchase for my 50-acre farm.',
      likes: 23,
      comments: 18,
      shares: 5,
      tags: ['fertilizer', 'advice', 'organic']
    },
    { 
      id: 3, 
      author: 'CropExpert', 
      avatar: 'CE',
      time: '1d ago',
      content: 'Just completed a 3-year crop rotation study. Happy to share detailed findings with anyone interested in sustainable farming practices! DM me 📊',
      likes: 89,
      comments: 24,
      shares: 15,
      tags: ['research', 'sustainability', 'rotation']
    }
  ];

  const categories = [
    { id: 'resources', label: 'Learning', icon: BookOpen },
    { id: 'community', label: 'Community', icon: Users },
    { id: 'trending', label: 'Trending', icon: TrendingUp }
  ];

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return '#22c55e';
      case 'Intermediate': return '#f59e0b';
      case 'Advanced': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <View className="flex-1 bg-gray-50">
      <StatusBar barStyle="light-content" backgroundColor="#16a34a" />
      
      {/* Header */}
      <LinearGradient
        colors={['#16a34a', '#22c55e']}
        className="pt-12 pb-6 px-5"
      >
        <Text className="text-2xl font-bold text-white mb-2">Explore & Learn</Text>
        <Text className="text-white/90">Discover knowledge and connect with farmers</Text>
      </LinearGradient>

      <ScrollView 
        className="flex-1" 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 100 }}
      >
        {/* Search Bar */}
        <View className="px-4 py-4">
          <Searchbar
            placeholder="Search for farming tips, crops, techniques..."
            onChangeText={setSearchQuery}
            value={searchQuery}
            style={{ backgroundColor: '#fff', elevation: 2 }}
            iconColor="#22c55e"
          />
        </View>

        {/* Tab Navigation */}
        <View className="px-4 mb-6">
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {categories.map((category) => (
              <TouchableOpacity
                key={category.id}
                onPress={() => setSelectedTab(category.id)}
                className="mr-3"
              >
                <Surface
                  className={`px-4 py-3 rounded-full flex-row items-center ${
                    selectedTab === category.id ? 'bg-green-600' : 'bg-white'
                  }`}
                  elevation={selectedTab === category.id ? 3 : 1}
                >
                  <category.icon 
                    size={18} 
                    color={selectedTab === category.id ? '#fff' : '#22c55e'} 
                  />
                  <Text 
                    className={`ml-2 font-medium ${
                      selectedTab === category.id ? 'text-white' : 'text-gray-800'
                    }`}
                  >
                    {category.label}
                  </Text>
                </Surface>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Learning Resources Tab */}
        {selectedTab === 'resources' && (
          <View className="px-4">
            <Text className="text-xl font-bold text-gray-800 mb-4">Featured Learning</Text>
            
            {learningResources.map((resource) => (
              <Card key={resource.id} className="mb-4 bg-white" elevation={3}>
                <Card.Content className="p-0">
                  <View className="flex-row">
                    {/* Thumbnail */}
                    <View className="w-24 h-24 bg-gray-100 items-center justify-center">
                      <Text className="text-3xl">{resource.thumbnail}</Text>
                      {resource.type === 'Video' && (
                        <View className="absolute bg-black/50 rounded-full p-1">
                          <Play size={16} color="#fff" />
                        </View>
                      )}
                    </View>

                    {/* Content */}
                    <View className="flex-1 p-4">
                      <View className="flex-row items-start justify-between mb-2">
                        <Text className="text-gray-800 font-semibold text-base flex-1 pr-2">
                          {resource.title}
                        </Text>
                        <Chip 
                          className="h-6"
                          textStyle={{ 
                            fontSize: 10, 
                            fontWeight: '600',
                            color: getDifficultyColor(resource.difficulty)
                          }}
                          style={{ backgroundColor: `${getDifficultyColor(resource.difficulty)}20` }}
                        >
                          {resource.difficulty}
                        </Chip>
                      </View>

                      <View className="flex-row items-center mb-2">
                        <resource.icon size={14} color="#22c55e" />
                        <Text className="text-green-600 text-sm font-medium ml-1">{resource.type}</Text>
                        <View className="w-1 h-1 bg-gray-400 rounded-full mx-2" />
                        <Clock size={14} color="#6b7280" />
                        <Text className="text-gray-600 text-sm ml-1">{resource.duration}</Text>
                      </View>

                      <View className="flex-row items-center justify-between">
                        <View>
                          <Text className="text-gray-500 text-xs">by {resource.author}</Text>
                          <Text className="text-gray-500 text-xs">{resource.views} views</Text>
                        </View>
                        <View className="flex-row items-center">
                          <Text className="text-yellow-500 font-medium text-sm">★ {resource.rating}</Text>
                        </View>
                      </View>
                    </View>
                  </View>
                </Card.Content>
              </Card>
            ))}
          </View>
        )}

        {/* Community Tab */}
        {selectedTab === 'community' && (
          <View className="px-4">
            <Text className="text-xl font-bold text-gray-800 mb-4">Community Feed</Text>
            
            {communityPosts.map((post) => (
              <Card key={post.id} className="mb-4 bg-white" elevation={3}>
                <Card.Content className="p-4">
                  {/* Post Header */}
                  <View className="flex-row items-center mb-3">
                    <Avatar.Text 
                      size={40} 
                      label={post.avatar}
                      className="bg-green-100"
                      labelStyle={{ color: '#22c55e', fontSize: 14, fontWeight: 'bold' }}
                    />
                    <View className="ml-3 flex-1">
                      <Text className="text-gray-800 font-semibold">{post.author}</Text>
                      <Text className="text-gray-500 text-sm">{post.time}</Text>
                    </View>
                  </View>

                  {/* Post Content */}
                  <Text className="text-gray-700 leading-6 mb-3">{post.content}</Text>

                  {/* Tags */}
                  <View className="flex-row flex-wrap mb-3">
                    {post.tags.map((tag, index) => (
                      <Chip 
                        key={index}
                        className="mr-2 mb-1 h-6 bg-gray-100"
                        textStyle={{ fontSize: 10, color: '#6b7280' }}
                      >
                        #{tag}
                      </Chip>
                    ))}
                  </View>

                  {/* Post Actions */}
                  <View className="flex-row items-center justify-between pt-3 border-t border-gray-100">
                    <TouchableOpacity className="flex-row items-center">
                      <Heart size={18} color="#ef4444" />
                      <Text className="text-gray-600 text-sm ml-1">{post.likes}</Text>
                    </TouchableOpacity>
                    <TouchableOpacity className="flex-row items-center">
                      <MessageCircle size={18} color="#6b7280" />
                      <Text className="text-gray-600 text-sm ml-1">{post.comments}</Text>
                    </TouchableOpacity>
                    <TouchableOpacity className="flex-row items-center">
                      <Share size={18} color="#6b7280" />
                      <Text className="text-gray-600 text-sm ml-1">{post.shares}</Text>
                    </TouchableOpacity>
                  </View>
                </Card.Content>
              </Card>
            ))}
          </View>
        )}

        {/* Trending Tab */}
        {selectedTab === 'trending' && (
          <View className="px-4">
            <Text className="text-xl font-bold text-gray-800 mb-4">Trending Topics</Text>
            
            <Card className="mb-4 bg-white" elevation={3}>
              <Card.Content className="p-6">
                <View className="items-center">
                  <TrendingUp size={48} color="#22c55e" />
                  <Text className="text-gray-800 font-semibold text-lg mt-4 mb-2">What's Hot</Text>
                  <Text className="text-gray-600 text-center">
                    Discover the latest trends, techniques, and discussions in modern agriculture
                  </Text>
                  <Button
                    mode="contained"
                    onPress={() => setSelectedTab('community')}
                    className="bg-green-600 mt-4"
                    contentStyle={{ paddingVertical: 4 }}
                  >
                    Explore Community
                  </Button>
                </View>
              </Card.Content>
            </Card>
          </View>
        )}
      </ScrollView>
    </View>
  );
}
