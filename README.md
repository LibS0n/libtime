# libtime

**What time is it right now, and how do I format it?**  
`libtime` gives you the answer – offline, fast, and without API keys.

A Python library that finds the **timezone** of any city worldwide (offline, using an embedded database) and optionally fetches the **current weather** via a free API.

## Features

- 🔍 **Timezone for any city** – offline, no internet required
- 🌍 **Three database sizes** – from "lite" (~2000 cities) to "full" (~150,000 cities)
- 🌦️ **Current weather** – async, uses Open‑Meteo (free, no API key)
- 🧩 **Minimal dependencies** – only `aiohttp` for weather, otherwise pure Python standard library
- ⚡ **Async API** – works well with Discord bots (Nextcord, discord.py) and other async apps

## Installation

```bash
pip install libtime
