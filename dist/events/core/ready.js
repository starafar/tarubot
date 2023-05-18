import { Events } from "discord.js";
import logger from "../../logging.js";
// Define the name of the event
export const name = Events.ClientReady;
// Specify that the event should run only once
export const once = true;
// Define the execute function that runs when the event is triggered
export function execute(client) {
    // Log a message indicating that the client has logged in
    logger.info(`Logged in as ${client.user?.tag}!`);
}
