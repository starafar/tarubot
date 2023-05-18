import { ChatInputCommandInteraction, SlashCommandBuilder } from "discord.js";

// Define the command metadata using SlashCommandBuilder
export const meta = new SlashCommandBuilder()
  .setName("ping")
  .setDescription("Check the bot's status and latency.");

// Define the execute function that runs when the command is executed
export async function execute(interaction: ChatInputCommandInteraction) {
  // Send an initial reply indicating that the bot is checking latency
  await interaction.reply({
    content: "Pong! Checking latency...",
    ephemeral: true,
  });

  // Calculate the latency and edit the previous reply with the result
  await interaction.editReply(
    `Pong! Latency: ${Date.now() - interaction.createdTimestamp} ms.`
  );
}
