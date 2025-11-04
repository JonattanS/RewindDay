import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { RootStackScreenProps } from '../../App';

type Props = RootStackScreenProps<'Home'>;

export function HomeScreen({ navigation }: Props) {
  return (
    <View style={styles.container}>
      <Ionicons name="time-outline" size={80} color="#6366f1" />
      <Text style={styles.title}>🕰️ RewindDay</Text>
      <Text style={styles.subtitle}>Reconstruye tus días del pasado</Text>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('Create')}
      >
        <Text style={styles.buttonText}>Crear Cápsula</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={[styles.button, { marginTop: 15 }]}
        onPress={() => navigation.navigate('History')}
      >
        <Text style={styles.buttonText}>Ver Historial</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
    padding: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1e293b',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    marginTop: 10,
  },
  button: {
    marginTop: 30,
    backgroundColor: '#6366f1',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 10,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
});
