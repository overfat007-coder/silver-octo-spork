const templateCache = new Map();

function addDecor(draw, theme) {
  if (theme === "birthday") {
    for (let i = 0; i < 6; i += 1) {
      draw.circle(18).fill(i % 2 === 0 ? "#ffd166" : "#ef476f").move(40 + i * 50, 35 + (i % 2) * 12);
    }
    draw.polygon("560,30 578,70 540,45 580,45 542,70").fill("#ffffff").opacity(0.8);
    return;
  }

  if (theme === "new_year") {
    for (let i = 0; i < 20; i += 1) {
      draw.circle(4).fill("#f8f9fa").move(20 + i * 28, 20 + (i % 5) * 12);
    }
    draw.rect(90, 90).radius(8).fill("#2a9d8f").move(470, 260);
    draw.rect(90, 14).fill("#e9c46a").move(470, 298);
    draw.rect(14, 90).fill("#e9c46a").move(508, 260);
    return;
  }

  draw.rect(540, 300).move(30, 30).radius(20).fill("none").stroke({ width: 2, color: "#ffffffaa" });
}

function renderDecorLayer(theme, width, height, createCanvas) {
  const draw = createCanvas(width, height);
  draw.rect(width, height).fill("none");
  addDecor(draw, theme);
  return draw.svg();
}

export function getOrCreateTemplate(theme, width, height, createCanvas) {
  const key = `${theme}:${width}:${height}`;
  if (!templateCache.has(key)) {
    templateCache.set(key, {
      gradient: `<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3a86ff"/><stop offset="100%" stop-color="#8338ec"/></linearGradient></defs>`,
      decorLayer: renderDecorLayer(theme, width, height, createCanvas),
    });
  }
  return templateCache.get(key);
}

export function cacheSize() {
  return templateCache.size;
}
