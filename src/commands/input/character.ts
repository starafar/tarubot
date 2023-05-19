import {
  ChatInputCommandInteraction,
  SlashCommandIntegerOption,
  SlashCommandSubcommandBuilder,
  SlashCommandBuilder,
  SlashCommandSubcommandGroupBuilder,
  SlashCommandStringOption,
  AutocompleteInteraction,
} from "discord.js";
import logger from "../../logging.js";

const serverList: Array<string> = [
  "Adamantoise",
  "Aegis",
  "Alexander",
  "Alpha",
  "Anima",
  "Asura",
  "Atomos",
  "Bahamut",
  "Balmung",
  "Behemoth",
  "Belias",
  "Bismarck",
  "Brynhildr",
  "Cactuar",
  "Carbuncle",
  "Cerberus",
  "Chocobo",
  "Coeurl",
  "Diabolos",
  "Durandal",
  "Excalibur",
  "Exodus",
  "Faerie",
  "Famfrit",
  "Fenrir",
  "Garuda",
  "Gilgamesh",
  "Goblin",
  "Gungnir",
  "Hades",
  "Halicarnassus",
  "Hyperion",
  "Ifrit",
  "Ixion",
  "Jenova",
  "Kujata",
  "Lamia",
  "Leviathan",
  "Lich",
  "Louisoix",
  "Maduin",
  "Malboro",
  "Mandragora",
  "Marilith",
  "Masamune",
  "Mateus",
  "Midgardsormr",
  "Moogle",
  "Odin",
  "Omega",
  "Pandaemonium",
  "Phantom",
  "Phoenix",
  "Ragnarok",
  "Raiden",
  "Ramuh",
  "Ravana",
  "Ridill",
  "Sagittarius",
  "Sargatanas",
  "Sephirot",
  "Seraph",
  "Shinryu",
  "Shiva",
  "Siren",
  "Sophia",
  "Spriggan",
  "Tiamat",
  "Titan",
  "Tonberry",
  "Twintania",
  "Typhon",
  "Ultima",
  "Ultros",
  "Unicorn",
  "Valefor",
  "Yojimbo",
  "Zalera",
  "Zeromus",
  "Zodiark",
  "Zurvan",
];

// Define the command metadata using SlashCommandBuilder
export const meta = new SlashCommandBuilder()
  .setName("character")
  .setDescription("Claim, manage, and release characters.")
  .addSubcommandGroup((subcommandGroup: SlashCommandSubcommandGroupBuilder) =>
    subcommandGroup
      .setName("claim")
      .setDescription("Claim a character.")
      .addSubcommand((subcommand: SlashCommandSubcommandBuilder) =>
        subcommand
          .setName("by_id")
          .setDescription("Claim a character by Lodestone ID.")
          .addIntegerOption((option: SlashCommandIntegerOption) =>
            option
              .setName("lodestone_id")
              .setDescription("The Lodestone ID of the character.")
              .setRequired(true)
          )
      )
      .addSubcommand((subcommand: SlashCommandSubcommandBuilder) =>
        subcommand
          .setName("by_name")
          .setDescription("Claim a character by name.")
          .addStringOption((option: SlashCommandStringOption) =>
            option
              .setName("first_name")
              .setDescription("The first name of the character.")
              .setRequired(true)
          )
          .addStringOption((option: SlashCommandStringOption) =>
            option
              .setName("last_name")
              .setDescription("The last name of the character.")
              .setRequired(true)
          )
          .addStringOption((option: SlashCommandStringOption) =>
            option
              .setName("server")
              .setDescription("The server of the character.")
              .setRequired(true)
              .setAutocomplete(true)
          )
      )
  );

// Define the execute function that runs when the command is executed
export async function execute(interaction: ChatInputCommandInteraction) {
  logger.debug(`Interaction: ${JSON.stringify(interaction)}`);
}

// Define the autocomplete function that runs when the command options are being autocompleted
export async function autocomplete(interaction: AutocompleteInteraction) {
  logger.debug(`Received autocomplete interaction: ${interaction.id}`);

  const focusedOption = interaction.options.getFocused(true);

  switch (interaction.options.getSubcommand(true)) {
    case "by_name":
      switch (focusedOption.name) {
        case "server":
          // Respond with server names that match the user's input
          await interaction.respond(
            serverList
              .map((server) => ({ name: server, value: server }))
              .filter((server) =>
                server.name
                  .toLowerCase()
                  .includes(focusedOption.value.toLowerCase())
              )
              .slice(0, 25)
          );
          break;

        default:
          break;
      }
  }
}
