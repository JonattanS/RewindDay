import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Capsule } from '../types/capsule.types';

interface CapsuleCardProps {
  capsule: Capsule;
  onPress: () => void;
  onDelete: () => void;
}

export default function CapsuleCard({
  capsule,
  onPress,
  onDelete,
}: CapsuleCardProps) {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress}>
      <View style={styles.cardHeader}>
        <View style={styles.cardTitleContainer}>
          <Ionicons name="time-outline" size={24} color="#6366f1" />
          <View style={styles.cardText}>
            <Text style={styles.cardTitle}>{capsule.title}</Text>
            <Text style={styles.cardDate}>{capsule.date}</Text>
          </View>
        </View>
        <TouchableOpacity onPress={onDelete}>
          <Ionicons name="trash-outline" size={24} color="#ef4444" />
        </TouchableOpacity>
      </View>

      <View style={styles.statusContainer}>
        <View style={[styles.statusBadge, getStatusStyle(capsule.status)]}>
          <Text style={styles.statusText}>{getStatusText(capsule.status)}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}

function getStatusStyle(status: string) {
  switch (status) {
    case 'completed':
      return { backgroundColor: '#d1fae5' };
    case 'processing':
      return { backgroundColor: '#fef3c7' };
    case 'failed':
      return { backgroundColor: '#fee2e2' };
    default:
      return { backgroundColor: '#e0e7ff' };
  }
}

function getStatusText(status: string) {
  switch (status) {
    case 'completed':
      return 'Completado';
    case 'processing':
      return 'Procesando';
    case 'failed':
      return 'Error';
    default:
      return 'Pendiente';
  }
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  cardText: {
    marginLeft: 12,
    flex: 1,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1e293b',
  },
  cardDate: {
    fontSize: 14,
    color: '#64748b',
    marginTop: 4,
  },
  statusContainer: {
    marginTop: 12,
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    alignSelf: 'flex-start',
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#1e293b',
  },
});
