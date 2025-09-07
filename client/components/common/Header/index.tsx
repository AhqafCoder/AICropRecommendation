import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Bell, Settings, User } from 'lucide-react-native';

interface HeaderProps {
  title?: string;
  showNotification?: boolean;
  showSettings?: boolean;
  showProfile?: boolean;
  onNotificationPress?: () => void;
  onSettingsPress?: () => void;
  onProfilePress?: () => void;
}

export default function Header({
  title = "AgriSmart",
  showNotification = true,
  showSettings = false,
  showProfile = false,
  onNotificationPress,
  onSettingsPress,
  onProfilePress
}: HeaderProps) {
  return (
    <View style={styles.container}>
      <View style={styles.leftSection}>
        <Text style={styles.title}>{title}</Text>
      </View>
      
      <View style={styles.rightSection}>
        {showNotification && (
          <TouchableOpacity style={styles.iconButton} onPress={onNotificationPress}>
            <Bell size={24} color="#fff" />
          </TouchableOpacity>
        )}
        
        {showSettings && (
          <TouchableOpacity style={styles.iconButton} onPress={onSettingsPress}>
            <Settings size={24} color="#fff" />
          </TouchableOpacity>
        )}
        
        {showProfile && (
          <TouchableOpacity style={styles.iconButton} onPress={onProfilePress}>
            <User size={24} color="#fff" />
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#4CAF50',
    paddingTop: 50,
    paddingBottom: 16,
    paddingHorizontal: 20,
  },
  leftSection: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  rightSection: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconButton: {
    padding: 8,
    marginLeft: 12,
  },
});
