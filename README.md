# feedctl

A terminal-based RSS reader built with [Textual](https://textual.textualize.io/).

## Features

- Browse RSS feeds in a clean three-column TUI
- Mark articles as read/unread (Space)
- Refresh feeds on demand (`r`)
- Theme switching via command palette (`Ctrl+P`)
- Articles stored locally in SQLite

## Installation

```bash
pip install feedctl
```

## Usage

```bash
feedctl
```

## Configuration

On first run, feedctl will ask you to set up your config file at `~/.config/feedctl/config.ini`:

```toml
[app]
theme = "default"

[[feeds]]
name = "Hacker News"
url = "https://news.ycombinator.com/rss"

[[feeds]]
name = "Reddit Programming"
url = "https://www.reddit.com/r/programming/.rss"
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
