const THEMES = new Set(["birthday", "new_year", "minimal"]);

export function validateCardPayload(payload) {
  if (!payload || typeof payload !== "object") {
    return { ok: false, error: "payload must be a JSON object" };
  }

  const { userName, message, theme } = payload;

  if (typeof userName !== "string" || userName.trim().length < 2 || userName.trim().length > 40) {
    return { ok: false, error: "userName must be 2..40 chars" };
  }

  if (typeof message !== "string" || message.trim().length < 5) {
    return { ok: false, error: "message must be at least 5 chars" };
  }

  if (message.length > 240) {
    return { ok: false, error: "message too long; max length is 240 chars" };
  }

  if (typeof theme !== "string" || !THEMES.has(theme)) {
    return { ok: false, error: "theme must be one of: birthday, new_year, minimal" };
  }

  return {
    ok: true,
    data: {
      userName: userName.trim(),
      message: message.trim(),
      theme,
    },
  };
}
