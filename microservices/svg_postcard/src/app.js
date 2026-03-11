import express from "express";

import { generateCardSvg } from "./svgCardService.js";
import { validateCardPayload } from "./validation.js";

export function createApp() {
  const app = express();
  app.use(express.json({ limit: "16kb" }));

  app.get("/health", (_req, res) => {
    res.json({ service: "svg-postcard", status: "ok" });
  });

  app.post("/api/v1/postcards/svg", (req, res) => {
    const validated = validateCardPayload(req.body);
    if (!validated.ok) {
      res.status(400).json({ error: validated.error });
      return;
    }

    try {
      const svg = generateCardSvg(validated.data);
      res.status(200).type("image/svg+xml").send(svg);
    } catch (error) {
      res.status(422).json({ error: error.message });
    }
  });

  app.use((err, _req, res, _next) => {
    res.status(500).json({ error: `internal server error: ${err.message}` });
  });

  return app;
}
