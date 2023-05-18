import { Client, Collection, GatewayIntentBits } from "discord.js";
import { globby } from "globby";
import config from "./config.js";
import logger from "./logging.js";
/**
 * Starts the Discord bot.
 * This function initializes the bot client, loads commands and events,
 * and logs in using the provided API token.
 */
async function start() {
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
        globby("./commands/chat/**/*.js", { cwd: "dist" }),
        globby("./commands/context/**/*.js", { cwd: "dist" }),
        globby("./events/**/*.js", { cwd: "dist" }),
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
    bot.login(config.discord.api.token);
}
// Export the start function as the default export of the module
export default start;
