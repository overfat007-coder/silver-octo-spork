import test from "node:test";
import assert from "node:assert/strict";
import request from "supertest";

import { createApp } from "../src/app.js";
import { cacheSize } from "../src/templateCache.js";

const app = createApp();

test("returns svg for valid input", async () => {
  const response = await request(app)
    .post("/api/v1/postcards/svg")
    .send({
      userName: "Анна",
      message: "С днем рождения! Пусть каждый день будет ярким и счастливым.",
      theme: "birthday",
    });

  assert.equal(response.status, 200);
  assert.match(response.headers["content-type"], /image\/svg\+xml/);
  assert.match(response.text, /<svg/);
});

test("rejects too long messages", async () => {
  const response = await request(app)
    .post("/api/v1/postcards/svg")
    .send({
      userName: "User",
      message: "x".repeat(241),
      theme: "minimal",
    });

  assert.equal(response.status, 400);
  assert.match(response.body.error, /too long/i);
});

test("caches templates in memory", async () => {
  const before = cacheSize();

  await request(app)
    .post("/api/v1/postcards/svg")
    .send({ userName: "Ilya", message: "Happy New Year and best wishes!", theme: "new_year" });

  const mid = cacheSize();

  await request(app)
    .post("/api/v1/postcards/svg")
    .send({ userName: "Ilya", message: "Another message", theme: "new_year" });

  const after = cacheSize();

  assert.ok(mid >= before);
  assert.equal(after, mid);
});
