import { createApp } from "./app.js";

const port = Number(process.env.PORT || 8010);
const app = createApp();

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`svg postcard service running on :${port}`);
});
