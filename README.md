# libtime

What time is it right now, and how do I format it?  
`libtime` gives you the answer – offline, fast, and without API keys.

A Python library that finds the **timezone** of any city worldwide (offline, using an embedded database), provides **local time formatting** (12h/24h, custom strftime), supports **optional calendar conversions** (Hijri, Jalali, Hebrew), and can fetch the **current weather** via a free API.

## Features

- Timezone for any city – offline, no internet required
- Three database sizes – from "lite" (~2000 cities) to "full" (~150,000 cities)
- Local time formatting – 12h/24h, with/without seconds, or any custom pattern
- Optional calendar conversions – Islamic (Hijri), Persian (Jalali), Hebrew
- Current weather – async, uses Open-Meteo (free, no API key)
- Minimal dependencies – only `aiohttp` for weather; calendars are optional extras
- Async API – works well with Discord bots (Nextcord, discord.py) and other async apps

## Installation

Basic installation (timezone + weather):

```bash
    pip install libtime
```

For optional calendar conversions (Hijri, Jalali, Hebrew):

```bash
    pip install libtime[calendar]
```

## Quickstart Examples

### 1. Timezone of a city

```python
    from libtime import timezone_for_city
    
    print(timezone_for_city("Berlin"))      # Europe/Berlin
    print(timezone_for_city("Tokyo"))       # Asia/Tokyo
    print(timezone_for_city("New York"))    # America/New_York
```

### 2. Get all city data (coordinates, country, timezone)

```python
    from libtime import resolve_city
    
    data = resolve_city("Cairo")
    print(data)
    # {
    #   'tz': 'Africa/Cairo',
    #   'lat': 30.0444,
    #   'lng': 31.2357,
    #   'country': 'EG'
    # }
```

### 3. Local time formatting

```python
    from libtime import local_time
    
    print(local_time("Berlin"))                      # 14:05:30 (24h with seconds)
    print(local_time("London", format="12h"))        # 02:05:30 PM
    print(local_time("New York", format="12h_no_sec")) # 02:05 PM
    print(local_time("Tokyo", format="%I:%M %p"))    # custom strftime -> 02:05 PM
```

### 4. Current weather (async)

```python
    import asyncio
    from libtime import get_current_weather, format_weather
    
    async def main():
        weather = await get_current_weather("Paris")
        if weather:
            print(format_weather(weather))   # "Rain, 12.3°C"
        else:
            print("City not found or API error")
    
    asyncio.run(main())
```

### 5. Optional calendar conversions (requires `libtime[calendar]`)

```python
    from libtime import local_datetime
    from libtime.calendar import to_hijri, to_jalali, to_hebrew
    
    dt = local_datetime("Cairo")
    if dt:
        print(to_hijri(dt))    # {'year': 1446, 'month': 9, 'month_name': 'Ramadan', 'day': 12}
        print(to_jalali(dt))   # {'year': 1404, 'month': 2, 'month_name': 'Ordibehesht', 'day': 22}
        print(to_hebrew(dt))   # {'year': 5784, 'month': 8, 'month_name': 'Iyar', 'day': 15}
```

### 6. Discord bot example (Nextcord)

```python
    import nextcord
    from nextcord.ext import commands
    from libtime import preload_database, timezone_for_city, local_time, get_current_weather
    
    bot = commands.Bot(command_prefix="!")
    
    @bot.event
    async def on_ready():
        preload_database("city")
        print(f"Bot {bot.user} is ready")
    
    @bot.command()
    async def time(ctx, *, city: str):
        tz = timezone_for_city(city)
        if not tz:
            await ctx.send(f"City `{city}` not found.")
            return
        local = local_time(city, format="12h")
        await ctx.send(f"**{city}**\nTimezone: `{tz}`\nLocal time: `{local}`")
    
    @bot.command()
    async def weather(ctx, *, city: str):
        w = await get_current_weather(city)
        if w:
            await ctx.send(f"**{city}**: {w['temperature']:.1f}°C")
        else:
            await ctx.send(f"No weather data for `{city}`.")
    
    bot.run("YOUR_TOKEN")
```

## Database Variants

`libtime` includes three pre‑built databases. Choose one with `preload_database()`:

| Variant | Size   | Contains                                                        |
|---------|--------|-----------------------------------------------------------------|
| `lite`  | 0.5 MB | ~2000 major cities (capitals + large cities), primary names only |
| `city`  | 2 MB   | ~135,000 cities, **multilingual** (all names from translations) |
| `full`  | 2.2 MB | Same as `city` plus `state` (province/state) and `capital` flag |

Preload a specific variant:

    from libtime import preload_database
    preload_database("full")   # or "city", "lite"

If you do not preload, the library automatically uses the largest available database (`full` > `city` > `lite`).

## Weather Notes

- Requires an **active internet connection**.
- **No API key required** – Open‑Meteo is completely free.
- Asynchronous – use `await get_current_weather("city")`.
- Weather codes are mapped to readable texts (see `libtime.WEATHER_CODES`).

## Credits

- City database: [dr5hn/countries-states-cities-database](https://github.com/dr5hn/countries-states-cities-database) (ODbL 1.0)
- Weather API: [Open-Meteo](https://open-meteo.com/) (free, no API key)
- HTTP client: [aiohttp](https://github.com/aio-libs/aiohttp) (Apache License 2.0)
- Optional calendars: [hijri-converter](https://pypi.org/project/hijri-converter/), [jdatetime](https://pypi.org/project/jdatetime/), [convertdate](https://pypi.org/project/convertdate/)

## License

MIT License – see [LICENSE](LICENSE) file.
