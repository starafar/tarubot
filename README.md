# TaruBot

TaruBot is designed for Discord servers that cater to players of Final Fantasy XIV: A Realm Reborn and its expansions.

The following functionality is planned:

- Event Planning/Party Finder
- Character/Free Company Search
- Character linking to an owner's Discord account
- Market search and various tools
  - There's a lot that can fall under this, to varying degrees of complexity. We'll see what I can do.
- Equipment tracking and goals
- Automatic role grant to FC members vs. guests based on Lodestone FC membership data
- And probably more.

Have ideas? Open an enhancement issue and we can work on it. Or write it yourself (TypeScript), and submit a PR.

## Hosting the Bot

TaruBot is intended to be self-hosted.

You'll need the following:

- A service to host the bot. That could be a server (at home, VPS, application hosting platform, whatever.)
- NodeJS v20
- A database server. This could be anything that works with Sequelize, but I recommended MariaDB or PostgreSQL. You could also use SQLite to store the data locally, but I don't recommend it for a bot you plan on actually using.

You can even use the same server to host the bot and the database. Just make sure that you're backing up the database regularly to avoid sadness.

## Get It Running

1. Make sure your hosting and database is configured.
2. Clone/download the repo to the hosting server.
3. In `dist/config`, copy or rename `local.yaml.template` to `local.yaml` and set the configuration appropriately.
4. Install dependencies via `npm install` or `yarn install`.
   - If you don't plan to make changes to the bot, you can run `npm install --production` or `yarn install --prod` to avoid the development dependencies.
5. Start the bot via `npm run start` or `yarn start`.
