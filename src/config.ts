import dotenv from "dotenv";

dotenv.config();

if (!process.env["TARUBOT_DISCORD_API_TOKEN"]) {
  throw new Error(
    "No Discord API token was provided. Check your configuration in .env or environment variables."
  );
}

if (!process.env["TARUBOT_DISCORD_APP_ID"]) {
  throw new Error(
    "No Discord app ID was provided. Check your configuration in .env or environment variables."
  );
}

if (
  process.env["TARUBOT_LOG_CONSOLE_ENABLED"] === "false" &&
  process.env["TARUBOT_LOG_FILE_ENABLED"] === "false"
) {
  throw new Error(
    "No logging output was enabled. Check your configuration in .env or environment variables."
  );
}

if (!process.env["TARUBOT_DB_DIALECT"]) {
  throw new Error(
    "No database dialect was provided. Check your configuration in .env or environment variables."
  );
}

export default {
  discord: {
    api: {
      token: process.env["TARUBOT_DISCORD_API_TOKEN"],
      appID: process.env["TARUBOT_DISCORD_APP_ID"],
    },
    guilds: process.env["TARUBOT_DISCORD_GUILDS"]?.split(","),
  },
  db: {
    database: process.env["TARUBOT_DB_DATABASE"] ?? "tarubot",
    username: process.env["TARUBOT_DB_USERNAME"] ?? "tarubot",
    password: process.env["TARUBOT_DB_PASSWORD"],
    host: process.env["TARUBOT_DB_HOST"],
    port:
      (process.env["TARUBOT_DB_PORT"] &&
        parseInt(process.env["TARUBOT_DB_PORT"])) ||
      undefined,
    dialect: process.env["TARUBOT_DB_DIALECT"],
  },
  log: {
    console: {
      enabled: process.env["TARUBOT_LOG_CONSOLE_ENABLED"] === "true",
      level: process.env["TARUBOT_LOG_CONSOLE_LEVEL"] ?? "info",
    },
    file: {
      enabled: process.env["TARUBOT_LOG_FILE_ENABLED"] === "true",
      level: process.env["TARUBOT_LOG_FILE_LEVEL"] ?? "info",
      path: process.env["TARUBOT_LOG_FILE_PATH"] ?? "./logs/tarubot.log",
    },
  },
};
