# Install the Wazza MCP server in Cline

Wazza is a hosted (remote) MCP server. There is nothing to download, build or run locally.

- Server URL: `https://api-pro.wazza.ai/v1/mcp`
- Transport: Streamable HTTP
- Auth: OAuth sign-in (preferred), or an API key sent as `Authorization: Bearer wz_live_...`

## Option 1: OAuth sign-in (no key to paste)

Add this entry to `cline_mcp_settings.json` (or use the Remote Servers tab: Server Name `wazza`,
Server URL as above, Transport Type "Streamable HTTP"):

```json
{
  "mcpServers": {
    "wazza": {
      "type": "streamableHttp",
      "url": "https://api-pro.wazza.ai/v1/mcp",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

The `type` field must be `streamableHttp`; without it Cline uses the legacy SSE transport, which
this server does not offer.

On the first call, Cline opens the Wazza sign-in page in the browser. The user signs in, picks the
workspace (they must be its owner or admin), the permissions, Live or Test, and an optional monthly
spend cap, then allows. If the browser does not open, use Cline's "Authorize OAuth" action for the
server.

## Option 2: API key

Ask the user for a Wazza API key (they make one at https://app.wazza.ai under Settings > API keys).
Never invent a key. Then use:

```json
{
  "mcpServers": {
    "wazza": {
      "type": "streamableHttp",
      "url": "https://api-pro.wazza.ai/v1/mcp",
      "headers": {
        "Authorization": "Bearer wz_live_THE_USER_KEY"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

A test key (`wz_test_...`) is free and returns sample files: it checks the setup, not real work.

## Check the install

Call the tool `list_tools`. It needs no credits. Then `get_balance` shows the credit balance.

## Rules for the agent

- Leave `autoApprove` empty. `start_run` and `chat_completion` spend credits; the user should
  confirm each one.
- Call `estimate_run` before `start_run` and tell the user the price.
- Runs are asynchronous: after `start_run`, call `get_run` until the status is `succeeded`,
  `failed` or `cancelled`.
- `create_topup_link` is listed only when the user gave the billing purchase permission. It makes a
  Stripe payment link and charges nothing; give the link to the user and never open it for them.

Docs: https://api-pro.wazza.ai/docs/guide and https://api-pro.wazza.ai/llms.txt
