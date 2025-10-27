import React, { useState } from "react";
import { View, Text, TextInput, Button, ScrollView, StyleSheet, Platform } from "react-native";
import { reconstructDay } from "./src/api";
export default function App() {
  const [date, setDate] = useState("2018-05-01");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const onSend = async () => {
    setBusy(true); setError(null);
    try { const data = await reconstructDay({ text: date }); setResult(data); }
    catch (e: any) { setError(e?.message ?? "Unknown error"); setResult(null); }
    finally { setBusy(false); }
  };
  return (<ScrollView contentContainerStyle={styles.wrap}>
      <Text style={styles.h1}>RewindDay – Capsule Reconstruct</Text>
      <Text style={styles.caption}>Enter a date (YYYY-MM-DD)</Text>
      <TextInput style={styles.input} value={date} onChangeText={setDate} autoCapitalize="none" placeholder="e.g. 2018-05-01" />
      <Button title={busy ? "Processing..." : "Reconstruct Day"} onPress={onSend} disabled={busy} />
      {error && <Text style={styles.error}>⚠️ {error}</Text>}
      {!!result && (<View style={styles.card}><Text selectable style={styles.mono}>{JSON.stringify(result, null, 2)}</Text></View>)}
      <Text style={styles.footer}>Platform: {Platform.OS}. API: http://localhost:8081 (iOS) or http://10.0.2.2:8081 (Android).</Text>
    </ScrollView>);
}
const styles = StyleSheet.create({
  wrap: { padding: 20, gap: 12 }, h1: { fontSize: 20, fontWeight: "600" }, caption: { opacity: 0.8 },
  input: { borderWidth: 1, borderColor: "#ccc", borderRadius: 8, padding: 10 },
  card: { marginTop: 14, padding: 12, borderWidth: 1, borderColor: "#e0e0e0", borderRadius: 8 },
  mono: { fontFamily: Platform.select({ ios: "Menlo", android: "monospace" }), fontSize: 12 },
  footer: { marginTop: 16, opacity: 0.7 }, error: { color: "#c00", marginTop: 8 }
});