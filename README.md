# feedr

A terminal-based RSS reader built with [Textual](https://textual.textualize.io/).

## Features

- Browse RSS feeds in a clean three-column TUI
- Mark articles as read/unread (Space)
- Refresh feeds on demand (`r`)
- Theme switching via command palette (`Ctrl+P`)
- Articles stored locally in SQLite

## Installation

```bash
pip install feedr
```

## Usage

```bash
feedr
```

## Configuration

On first run, feedr will ask you to set up your config file at `~/.config/feedr/config.ini`:

```ini
[app]
name = feedr

[feeds]
Hacker News = https://news.ycombinator.com/rss
```

## Keybindings

| Key | Action |
|-----|--------|
| `→` | Focus articles column |
| `←` | Focus feeds column |
| `Space` | Mark article as read |
| `r` | Refresh feeds |
| `Ctrl+P` | Command palette (theme switcher, etc.) |
| `q` | Quit |
