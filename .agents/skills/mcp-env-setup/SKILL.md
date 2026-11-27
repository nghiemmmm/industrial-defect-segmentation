---
name: mcp-env-setup
description: >-
  Set up and validate project-scoped STDIO MCP servers in Antigravity that load
  API tokens from a workspace .env file without hardcoding or exposing secrets.
  Use when configuring npx-based MCP servers (such as Notion, GitHub, or other
  official MCP packages) for a specific repository.
---

# Project-Scoped MCP Server Setup with `.env` Secrets

## Security Invariants (Always Enforce)
1. **Never read `.env` with `read_file`** or print/log any secret value in shell output.
2. Verify `.env` existence and required keys with boolean-only checks (e.g. `Test-Path ".env"` and regex match returning `True`/`False`).
3. Ensure `.env` is ignored by Git (`git check-ignore -v .env`). If missing from `.gitignore`, add `.env`, `.env.*`, and `!.env.example` before proceeding.
4. Never overwrite existing global or plugin MCP configs; always package project-specific servers in their own workspace plugin directory.

## Step 1: Inventory Existing Plugins & Check Collisions
Query the Antigravity Language Server `GetAllPlugins` RPC with the active workspace URI (`file:///...`) and inspect `name`, `dir`, and `mcpServers[].serverName` (not `.name`) to ensure no plugin or server name collisions.

## Step 2: Create a Workspace Plugin Bundle
Create `.agents/plugins/<plugin-name>/` with three files:

1. **`plugin.json`** (only valid top-level fields: `name`, `displayName`, `description`):
   ```json
   {
     "name": "<plugin-name>",
     "displayName": "<Display Name>",
     "description": "Project-scoped <Service> MCP Server loading <ENV_VAR> from the workspace .env file."
   }
   ```

2. **`load-env.cjs`** (silent, zero-dependency CommonJS preload):
   - Why: Antigravity does not auto-load `.env` into `mcp_config.json`, and Node.js v22 rejects `--env-file=` inside `NODE_OPTIONS`.
   - Behavior: If `!process.env.<ENV_VAR>`, read `path.resolve(__dirname, "..", "..", "..", ".env")`, parse `<ENV_VAR>` (handling comments, `export `, CRLF, and optional quotes), and set `process.env.<ENV_VAR>`.
   - **Critical:** Never write anything to `stdout` or `stderr` (keeps STDIO JSON-RPC clean and prevents secret leakage).

3. **`mcp_config.json`**:
   ```json
   {
     "mcpServers": {
       "<server-key>": {
         "command": "npx",
         "args": ["-y", "<@scope/mcp-package>"],
         "env": {
           "NODE_OPTIONS": "--require=<absolute-forward-slash-path>/.agents/plugins/<plugin-name>/load-env.cjs"
         }
       }
     }
   }
   ```
   - Use forward slashes in `--require=...` on Windows to avoid backslash escaping issues in `NODE_OPTIONS`.

## Step 3: Validate End-to-End
1. **Preload check:** Run `node -e "console.log(Boolean(process.env.<ENV_VAR>))"` with `NODE_OPTIONS=--require=...` and confirm `true`.
2. **Discovery check:** Re-run `GetAllPlugins` with `workspaceUris` and verify the plugin appears with `CUSTOMIZATION_SCOPE_WORKSPACE` and the expected `mcpServers[].serverName`.
3. **STDIO handshake & read-only call:** Spawn `npx -y <package>` with the exact `NODE_OPTIONS` from `mcp_config.json` and send:
   - `initialize`
   - `notifications/initialized`
   - `tools/list`
   - One safe, read-only `tools/call` (e.g., identity/self or limited search)
   - Redact any token-like patterns if logging `stderr`.
4. **Git check:** Run `git status --short` and `git check-ignore -v .env` to confirm no secrets are staged or tracked.
