// Import necessary dependencies and modules
import {
  REST,
  RESTPostAPIApplicationCommandsJSONBody,
  Routes,
} from "discord.js";
import { globby } from "globby";
import { IChatInputCommand, IContextMenuCommand } from "./types.js";
import config from "./config.js";
import logger from "./logging.js";

/**
 * Deploys the Discord application commands.
 * This function registers the application commands for the bot on Discord.
 * It checks the configuration for the required API token and application ID,
 * and loads the command files from the specified directory.
 * Then it registers the commands either globally or for specific guilds.
 */
async function deploy() {
  // Find command files using glob pattern
  const chatCommandFiles = await globby("./commands/chat/**/*.js", {
    cwd: "dist",
  });
  const contextMenuCommandFiles = await globby("./commands/context/**/*.js", {
    cwd: "dist",
  });

  const commandFiles = [...chatCommandFiles, ...contextMenuCommandFiles];

  // Array to store the application commands
  const commands: RESTPostAPIApplicationCommandsJSONBody[] = await Promise.all(
    commandFiles.map(async (commandFile) => {
      logger.debug(`Loading ${commandFile}...`);
      const command: IChatInputCommand | IContextMenuCommand = await import(
        commandFile
      );
      logger.debug(`Loaded command ${command.meta.name}.`);
      return command.meta.toJSON();
    })
  );

  logger.debug(`Loaded ${commands.length} commands.`);

  // Create a new REST instance and set the token
  const rest = new REST().setToken(config.discord.api.token);

  // Check if guild-specific commands are specified in the configuration
  if (config.discord.guilds) {
    // Register application commands for each specified guild
    for (const guildId of config.discord.guilds) {
      logger.info(`Registering application commands for guild ${guildId}...`);

      // Send a PUT request to register the commands for the guild
      await rest.put(
        Routes.applicationGuildCommands(config.discord.api.appID, guildId),
        {
          body: commands,
        }
      );

      logger.info(
        `Successfully registered application commands for guild ${guildId}.`
      );
    }
  } else {
    // Register application commands globally
    logger.info("Registering application commands...");

    // Send a PUT request to register the commands globally
    await rest.put(Routes.applicationCommands(config.discord.api.appID), {
      body: commands,
    });

    logger.info("Successfully registered application commands.");
  }
}

// Export the deploy function as the default export of the module
export default deploy;
