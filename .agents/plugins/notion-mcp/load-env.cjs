"use strict";

const fs = require("node:fs");
const path = require("node:path");

// Preload NOTION_TOKEN from the workspace root .env file without logging or
// writing anything to stdout/stderr (required for clean MCP STDIO transport).
if (!process.env.NOTION_TOKEN) {
  const envPath = path.resolve(__dirname, "..", "..", "..", ".env");
  try {
    const content = fs.readFileSync(envPath, "utf8");
    for (const rawLine of content.split(/\r?\n/)) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) continue;
      const match = line.match(/^(?:export\s+)?NOTION_TOKEN\s*=\s*(.*)$/);
      if (!match) continue;
      let value = match[1].trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      if (value) {
        process.env.NOTION_TOKEN = value;
      }
      break;
    }
  } catch {
    // Intentionally silent: let the MCP server handle missing credentials.
  }
}
