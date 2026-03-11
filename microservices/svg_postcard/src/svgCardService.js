import { SVG, registerWindow } from "@svgdotjs/svg.js";
import { createSVGWindow } from "svgdom";

import { getOrCreateTemplate } from "./templateCache.js";
import { wrapText } from "./wrapText.js";

const WIDTH = 600;
const HEIGHT = 360;

function createCanvas(width, height) {
  const window = createSVGWindow();
  const { document } = window;
  registerWindow(window, document);
  return SVG(document.documentElement).size(width, height);
}

export function generateCardSvg({ userName, message, theme }) {
  const draw = createCanvas(WIDTH, HEIGHT);
  const template = getOrCreateTemplate(theme, WIDTH, HEIGHT, createCanvas);

  draw.svg(`<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}">${template.gradient}${template.decorLayer}</svg>`);
  draw.rect(WIDTH, HEIGHT).fill("url(#bg)").back();

  draw.text(`Для: ${userName}`).font({
    size: 30,
    family: "Arial",
    weight: "bold",
  }).fill("#ffffff").move(40, 110);

  const lines = wrapText(message, 34);
  const maxLines = 6;
  if (lines.length > maxLines) {
    throw new Error(`message cannot fit: max ${maxLines} lines`);
  }

  const baseY = 165;
  lines.forEach((line, index) => {
    draw.text(line).font({ size: 23, family: "Arial" }).fill("#f8f9fa").move(40, baseY + index * 34);
  });

  return draw.svg();
}
