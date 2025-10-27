import axios from "axios";
import { API_BASE } from "./config";
export const api = axios.create({ baseURL: API_BASE, timeout: 10000 });
export async function reconstructDay(payload: { text: string }) {
  const { data } = await api.post("/capsule/reconstruct", payload);
  return data;
}