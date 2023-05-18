// Import necessary dependencies and modules
import { REST, Routes } from "discord.js";
import { globby } from "globby";
import config from "config";
import logger from "./logging.js";
/**
 * Deploys the Discord application commands.
 * This function registers the application commands for the bot on Discord.
 * It checks the configuration for the required API token and application ID,
 * and loads the command files from the specified directory.
 * Then it registers the commands either globally or for specific guilds.
 */
async function deploy() {
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
    logger.crit(
      `The following config entries are missing: ${missingConfigEntries.join(
        ", "
      )}`
    );
    return;
  }
  // Find command files using glob pattern
  const commandFiles = await globby("./commands/**/*.js", { cwd: "dist" });
  // Array to store the application commands
  const commands = await Promise.all(
    commandFiles.map(async (commandFile) => {
      logger.debug(`Loading ${commandFile}...`);
      const command = await import(commandFile);
      logger.debug(`Loaded command ${command.meta.name}.`);
      return command.meta.toJSON();
    })
  );
  logger.debug(`Loaded ${commands.length} commands.`);
  // Create a new REST instance and set the token
  const rest = new REST().setToken(config.get("discord.api.token"));
  // Check if guild-specific commands are specified in the configuration
  if (config.has("discord.guilds")) {
    // Register application commands for each specified guild
    for (const guildId of config.get("discord.guilds")) {
      logger.info(`Registering application commands for guild ${guildId}...`);
      // Send a PUT request to register the commands for the guild
      await rest.put(
        Routes.applicationGuildCommands(
          config.get("discord.api.app_id"),
          guildId
        ),
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
    await rest.put(
      Routes.applicationCommands(config.get("discord.api.app_id")),
      {
        body: commands,
      }
    );
    logger.info("Successfully registered application commands.");
  }
}
// Export the deploy function as the default export of the module
export default deploy;
