import { Client, Collection, GatewayIntentBits } from "discord.js";
import { IChatInputCommand, IEvent } from "./types";
import { globby } from "globby";
import config from "config";
import logger from "./logging.js";

/**
 * Starts the Discord bot.
 * This function initializes the bot client, loads commands and events,
 * and logs in using the provided API token.
 */
async function start() {
  // Array to store missing configuration entries
  const missingConfigEntries = Array<string>();

  // Check if the API token is present in the configuration
  if (!config.has("discord.api.token") || !config.get("discord.api.token")) {
    missingConfigEntries.push("API token");
  }

  // Check if the application ID is present in the configuration
  if (!config.has("discord.api.app_id") || !config.get("discord.api.app_id")) {
    missingConfigEntries.push("application ID");
  }

  // If any configuration entries are missing, log an error and return
  if (missingConfigEntries.length > 0) {
    logger.crit(
      `The following config entries are missing: ${missingConfigEntries.join(
        ", "
      )}`
    );
    return;
  }

  // Define the gateway intents for the bot
  const gatewayIntents = [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildScheduledEvents,
  ];

  // Create a new bot client with the specified intents
  const bot = new Client({
    intents: gatewayIntents,
  });

  // Create a collection to store chat input commands
  bot.chatInputCommands = new Collection<string, IChatInputCommand>();

  // Load command files and event files using glob patterns
  const [commandFiles, eventFiles] = await Promise.all([
    globby("./commands/**/*.js"),
    globby("./events/**/*.js"),
  ]);

  logger.debug(`Loading ${commandFiles.length} commands from ${commandFiles}.`);
  logger.debug(`Loading ${eventFiles.length} events from ${eventFiles}.`);

  // Load and register commands
  const loadCommands = Promise.all(
    commandFiles.map(async (commandFile) => {
      logger.debug(`Loading ${commandFile}...`);
      const command: IChatInputCommand = await import(commandFile);
      logger.debug(`Loaded command ${command.meta.name}.`);

      bot.chatInputCommands.set(command.meta.name, command);
    })
  );

  // Load and register events
  const loadEvents = Promise.all(
    eventFiles.map(async (eventFile) => {
      logger.debug(`Loading ${eventFile}...`);
      const event: IEvent = await import(eventFile);
      logger.debug(`Loaded event ${event.name}.`);

      if (event.once) {
        bot.once(event.name, (...args) => event.execute(...args));
      } else {
        bot.on(event.name, (...args) => event.execute(...args));
      }
    })
  );

  // Wait for commands and events to be loaded
  await Promise.all([loadCommands, loadEvents]);

  // Log in to Discord using the API token from the configuration
  bot.login(config.get("discord.api.token"));
}

// Export the start function as the default export of the module
export default start;
