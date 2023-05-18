import { Events } from "discord.js";
import logger from "../../logging.js";
// Define the name of the event
export const name = Events.InteractionCreate;
// Specify that the event should not run only once
export const once = false;
// Define the execute function that runs when the event is triggered
export function execute(interaction) {
    // Check if the interaction is a chat input command
    if (interaction.isChatInputCommand()) {
        // Get the command from the client's chatInputCommands collection
        const command = interaction.client.chatInputCommands.get(interaction.commandName);
        // If the command does not exist, return
        if (!command) {
            return;
        }
        try {
            // Execute the command with the interaction as the parameter
            command.execute(interaction);
        }
        catch (error) {
            // Log the error and send an error message as a reply
            logger.error(error);
            interaction.reply({
                content: "There was an error while executing this command!",
                ephemeral: true,
            });
        }
    }
}
