import { Platform } from "react-native";
const LAN_IP = "192.168.1.50";
export const API_BASE =
  Platform.OS === "ios"
    ? "http://localhost:8081"
    : Platform.OS === "android"
      ? "http://10.0.2.2:8081"
      : `http://${LAN_IP}:8081`;