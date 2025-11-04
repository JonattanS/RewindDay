import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator, NativeStackScreenProps } from '@react-navigation/native-stack';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// ========================
// TIPOS DE NAVEGACIÓN
// ========================

export type RootStackParamList = {
  Home: undefined;
  Create: undefined;
  View: { id: string };
  History: undefined;
  Video: { videoId: string };
};

export type RootStackScreenProps<T extends keyof RootStackParamList> = 
  NativeStackScreenProps<RootStackParamList, T>;

// ========================
// NAVEGADOR
// ========================

const Stack = createNativeStackNavigator<RootStackParamList>();

// ========================
// PANTALLAS
// ========================

function HomeScreen({ navigation }: RootStackScreenProps<'Home'>) {
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

function CreateScreen({ navigation }: RootStackScreenProps<'Create'>) {
  return (
    <View style={styles.container}>
      <Ionicons name="create-outline" size={80} color="#6366f1" />
      <Text style={styles.title}>Crear Cápsula</Text>
      <Text style={styles.subtitle}>Próximamente: Generador de Videos con IA</Text>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Volver</Text>
      </TouchableOpacity>
    </View>
  );
}

function HistoryScreen({ navigation }: RootStackScreenProps<'History'>) {
  return (
    <View style={styles.container}>
      <Ionicons name="list-outline" size={80} color="#6366f1" />
      <Text style={styles.title}>Historial</Text>
      <Text style={styles.subtitle}>Tus cápsulas guardadas</Text>
      
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Volver</Text>
      </TouchableOpacity>
    </View>
  );
}

// ========================
// APP PRINCIPAL
// ========================

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: {
            backgroundColor: '#6366f1',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
            fontSize: 18,
          },
          headerTitleAlign: 'center',
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="Create"
          component={CreateScreen}
          options={{
            title: 'Crear Cápsula',
          }}
        />
        <Stack.Screen
          name="History"
          component={HistoryScreen}
          options={{
            title: 'Historial',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// ========================
// ESTILOS
// ========================

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
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    marginTop: 10,
    textAlign: 'center',
  },
  button: {
    marginTop: 30,
    backgroundColor: '#6366f1',
    paddingHorizontal: 40,
    paddingVertical: 15,
    borderRadius: 10,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
});
