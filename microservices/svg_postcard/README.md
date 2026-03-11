# Dynamic SVG postcard service (Node.js)

HTTP endpoint that accepts JSON and returns generated SVG postcard.

## Endpoint
- `POST /api/v1/postcards/svg`

Body:
```json
{
  "userName": "Анна",
  "message": "С днем рождения! Пусть каждый день будет ярким.",
  "theme": "birthday"
}
```

Themes:
- `birthday`
- `new_year`
- `minimal`

## Features
- SVG generation using `@svgdotjs/svg.js` + `svgdom`
- layered rendering: gradient background + themed decor + wrapped text
- input validation + error handling for overlong message
- in-memory template cache by `theme:width:height`

## Run
```bash
npm install
npm start
```

## Test
```bash
npm test
```
