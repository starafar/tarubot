import { Client, Collection, GatewayIntentBits } from "discord.js";
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
    const missingConfigEntries = Array();
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
        logger.crit(`The following config entries are missing: ${missingConfigEntries.join(", ")}`);
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
    bot.chatInputCommands = new Collection();
    bot.contextMenuCommands = new Collection();
    // Load command files and event files using glob patterns
    const [chatInputCommandFiles, contextMenuCommandFiles, eventFiles] = await Promise.all([
        globby("./commands/chat/**/*.js"),
        globby("./commands/context/**/*.js"),
        globby("./events/**/*.js"),
    ]);
    logger.debug(`Loading ${chatInputCommandFiles.length} chat input commands from ${chatInputCommandFiles}.`);
    logger.debug(`Loading ${contextMenuCommandFiles.length} context menu commands from ${contextMenuCommandFiles}.`);
    logger.debug(`Loading ${eventFiles.length} events from ${eventFiles}.`);
    // Load and register commands
    const loadChatInputCommands = Promise.all(chatInputCommandFiles.map(async (chatInputCommandFile) => {
        logger.debug(`Loading ${chatInputCommandFile}...`);
        const chatInputCommand = await import(chatInputCommandFile);
        logger.debug(`Loaded command ${chatInputCommand.meta.name}.`);
        bot.chatInputCommands.set(chatInputCommand.meta.name, chatInputCommand);
    }));
    const loadContextMenuCommands = Promise.all(contextMenuCommandFiles.map(async (contextMenuCommandFile) => {
        logger.debug(`Loading ${contextMenuCommandFile}...`);
        const contextMenuCommand = await import(contextMenuCommandFile);
        logger.debug(`Loaded command ${contextMenuCommand.meta.name}.`);
        bot.contextMenuCommands.set(contextMenuCommand.meta.name, contextMenuCommand);
    }));
    // Load and register events
    const loadEvents = Promise.all(eventFiles.map(async (eventFile) => {
        logger.debug(`Loading ${eventFile}...`);
        const event = await import(eventFile);
        logger.debug(`Loaded event ${event.name}.`);
        if (event.once) {
            bot.once(event.name, (...args) => event.execute(...args));
        }
        else {
            bot.on(event.name, (...args) => event.execute(...args));
        }
    }));
    // Wait for commands and events to be loaded
    await Promise.all([
        loadChatInputCommands,
        loadContextMenuCommands,
        loadEvents,
    ]);
    // Log in to Discord using the API token from the configuration
    bot.login(config.get("discord.api.token"));
}
// Export the start function as the default export of the module
export default start;
