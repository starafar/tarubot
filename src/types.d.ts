import {
  AutocompleteInteraction,
  ChatInputCommandInteraction,
  ContextMenuCommandBuilder,
  ContextMenuCommandInteraction,
  MessageContextMenuCommandInteraction,
  SlashCommandBuilder,
  SlashCommandSubcommandBuilder,
  UserContextMenuCommandInteraction,
} from "discord.js";

// Define an interface for events
interface IEvent {
  name: string; // Name of the event
  once: boolean; // Whether the event runs only once
  execute: (...args: any[]) => void; // Function to execute when the event is triggered
}

// Define an interface for chat input commands
interface IChatInputCommand {
  meta: SlashCommandBuilder; // Metadata of the command
  execute: (interaction: ChatInputCommandInteraction) => void; // Function to execute when the command is triggered
  autocomplete?: (interaction: AutocompleteInteraction) => void;
}

// Define an interface for chat input commands
interface IContextMenuCommand {
  meta: ContextMenuCommandBuilder; // Metadata of the command
  execute: (interaction: ContextMenuCommandInteraction) => void; // Function to execute when the command is triggered
}

// Extend the "discord.js" module to add custom typings
declare module "discord.js" {
  export interface Client {
    chatInputCommands: Collection<string, IChatInputCommand>; // Property to store chat input commands associated with the client
    contextMenuCommands: Collection<string, IContextMenuCommand>; // Property to store user context menu commands associated with the client
  }
}
