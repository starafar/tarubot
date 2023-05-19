import {
  ChatInputCommandInteraction,
  ContextMenuCommandInteraction,
  Events,
  Interaction,
} from "discord.js";
import logger from "../../logging.js";
import { IChatInputCommand, IContextMenuCommand } from "../../types.js";

// Define the name of the event
export const name = Events.InteractionCreate;

// Specify that the event should not run only once
export const once = false;

// Define the execute function that runs when the event is triggered
export function execute(interaction: Interaction) {
  // If the interaction is not a command, return

  if (interaction.isCommand()) {
    if (interaction.isChatInputCommand()) {
      const command: IChatInputCommand =
        interaction.client.chatInputCommands.get(interaction.commandName);

      try {
        // Execute the command with the interaction as the parameter
        (command as IChatInputCommand).execute(
          interaction as ChatInputCommandInteraction
        );
      } catch (error) {
        // Log the error and send an error message as a reply
        logger.error(error);
        interaction.reply({
          content: "There was an error while executing this command!",
          ephemeral: true,
        });
      }
    } else if (interaction.isUserContextMenuCommand()) {
      const command: IContextMenuCommand =
        interaction.client.contextMenuCommands.get(interaction.commandName);

      try {
        // Execute the command with the interaction as the parameter
        (command as IContextMenuCommand).execute(
          interaction as ContextMenuCommandInteraction
        );
      } catch (error) {
        // Log the error and send an error message as a reply
        logger.error(error);
        interaction.reply({
          content: "There was an error while executing this command!",
          ephemeral: true,
        });
      }
    }
  } else if (interaction.isAutocomplete()) {
    const command: IChatInputCommand = interaction.client.chatInputCommands.get(
      interaction.commandName
    );

    if (!command.autocomplete) {
      logger.warn(
        `Autocomplete interaction received for command "${interaction.commandName}" but no autocomplete function is defined.`
      );
      return;
    }

    try {
      command.autocomplete(interaction);
    } catch (error) {
      logger.error(error);
    }
  }
}
