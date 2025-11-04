import React from 'react';
import { View, Text, TextInput, StyleSheet } from 'react-native';

interface DatePickerProps {
  value: string;
  onChange: (text: string) => void;
  label?: string;
}

export default function DatePicker({ value, onChange, label }: DatePickerProps) {
  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <TextInput
        style={styles.input}
        placeholder="YYYY-MM-DD (Ej: 2024-12-25)"
        value={value}
        onChangeText={onChange}
        keyboardType="numbers-and-punctuation"
      />
      <Text style={styles.hint}>Formato: Año-Mes-Día</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  hint: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 4,
  },
});
