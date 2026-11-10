# Wazza skills

Your agent can't watch video. Wazza measures it.

Skills for coding agents (Claude Code, Codex, Cursor and others) that call
[Wazza](https://app.wazza.ai/skills)'s tools: measure a render for loudness, flashing, colour levels
and file specs, then turn long video into shorts, add sound, and dub. Each skill is one
`SKILL.md` your agent reads: when to use it, which Wazza tools to call, what to do with the result.

Your agent quotes the price before every run. 1 credit = 1 US cent, prepaid, no subscription.
Each connection has a monthly spend cap you set, which the agent cannot change.

## Install

**Claude Code** (the plugin also connects the Wazza MCP server; the first call opens a sign-in
where you pick the workspace, Test or Live, and a monthly cap):

```
/plugin marketplace add Wazza-AI/skills
/plugin install wazza@wazza
```

**Codex, Cursor and others**: add the MCP server `https://api-pro.wazza.ai/v1/mcp` in your client's
MCP config, then install the skills with [`skills`](https://github.com/vercel-labs/skills):

```sh
npx skills add Wazza-AI/skills
```

Then ask your agent: `check out.mp4 with Wazza`.

Test keys (`wz_test_…`) are free and return sample files: they check your setup, not your video.

## Skills

| Skill | What it does |
|---|---|
| [`wazza-check`](skills/wazza-check/SKILL.md) | Measures a render against delivery rules (loudness, flashing, colour levels, file specs) and fixes what fails. |
| [`wazza-shorts`](skills/wazza-shorts/SKILL.md) | Long video to vertical 9:16 shorts with burned-in captions. Your agent picks the moments from the transcript. |
| [`wazza-unslop`](skills/wazza-unslop/SKILL.md) | Makes generated shots stop reading as generated: a critique of all shots, then its fix applied to each shot that needs one. |
| [`wazza-sound`](skills/wazza-sound/SKILL.md) | Foley written to the picture, sound effects and music, mixed by your agent with ffmpeg. |
| [`wazza-dub`](skills/wazza-dub/SKILL.md) | Dubs a video into other languages, one run per language, with subtitles, and checks each version. The lips do not change. |

The full list, including what is planned, is [`index.json`](index.json). `python3 scripts/check.py`
keeps it in step with the skill folders.

A pass from `wazza-check` is a measurement against the rules it lists, not a safety or compliance
certificate.
