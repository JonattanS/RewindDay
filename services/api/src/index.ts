import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import axios from "axios";
dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());
const PORT = process.env.PORT || 8080;
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || "http://localhost:8000";
app.get("/health", (_req, res) => res.json({ ok: true, name: "RewindDay-api" }));
app.post("/capsule/reconstruct", async (req, res) => {
  try { const r = await axios.post(`${AI_SERVICE_URL}/capsule/reconstruct`, req.body); res.json(r.data); }
  catch (e: any) { res.status(500).json({ error: e.message }); }
});
app.listen(PORT, () => console.log("RewindDay API on " + PORT));
