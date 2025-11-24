# RemindMe-Bot
Discord Bot for keeping track of various things such as shows to watch and books to read. It also sends an egg emoji (🥚) when someone says egg.

## How It's Made
- Technologies Used: `Python, JSON`

- Uses discord.ext.commands to define commands such as /watchlist, /watchlistshow, and /watchlistremove.
- Watchlist system writes entries to the json file. From that file, it reads and displays them with timestamps and authors.
- To remove an item from the watchlist, it uses the ID. 
- Writes bot events, command usage, and debug info to discord.log using Python’s logging module.

## Current Commands
- `/watchlist` or `/wl`
    - Adds a new entry to the watchlist.
- `/watchlistshow` or `/wlshow`
    - Displays the entire watchlist, paginated in chunks.
- `/watchlistremove` <id> or `/wlremove` <id>
    - Removes an entry by its numbered position.

## Future Implementations
- Deploy the bot so it runs 24/7 (e.g., Render, Railway, or another hosting platform)
- Separate lists for different categories (books, movies, shows, etc.)
- A /help command that lists all bot commands with descriptions
- Limit the max number of watchlist entries
- Integrate with an external data source (Google Sheets, Notion API, etc.) for more robust storage