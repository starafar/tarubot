import {
  ChatInputCommandInteraction,
  SlashCommandIntegerOption,
  SlashCommandStringOption,
  SlashCommandSubcommandBuilder,
  SlashCommandBuilder,
} from "discord.js";
import logger from "../../logging.js";

// Define the command metadata using SlashCommandBuilder
export const meta = new SlashCommandBuilder()
  .setName("event")
  .setDescription("Create, manage, or delete events.")
  .addSubcommand((subcommand: SlashCommandSubcommandBuilder) =>
    subcommand
      .setName("create")
      .setDescription("Create a new event.")
      .addStringOption((option: SlashCommandStringOption) =>
        option
          .setName("name")
          .setDescription("The name of the event.")
          .setRequired(true)
      )
      .addStringOption((option: SlashCommandStringOption) =>
        option
          .setName("date")
          .setDescription("The date of the event.")
          .setRequired(true)
      )
      .addStringOption((option: SlashCommandStringOption) =>
        option
          .setName("time")
          .setDescription("The time of the event.")
          .setRequired(true)
      )
      .addStringOption((option: SlashCommandStringOption) =>
        option
          .setName("description")
          .setDescription("The description of the event.")
          .setRequired(false)
      )
      .addIntegerOption((option: SlashCommandIntegerOption) =>
        option
          .setName("duration")
          .setDescription("The duration of the event in minutes.")
          .setRequired(false)
      )
  );

// Define the execute function that runs when the command is executed
export async function execute(interaction: ChatInputCommandInteraction) {
  logger.debug(`Interaction: ${JSON.stringify(interaction)}`);

  switch (interaction.options.getSubcommand()) {
    case "create":
      await interaction.reply("Event created.");
      break;
    default:
      await interaction.reply("Unknown subcommand.");
      break;
  }
}
