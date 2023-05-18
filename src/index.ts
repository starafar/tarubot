import start from "./start.js";
import deploy from "./deploy.js";
import logger from "./logging.js";

// Get command line arguments
const [, , command] = process.argv;

// Check the command and execute
if (command === "start") {
  logger.info("Starting bot...");
  await start();
} else if (command === "deploy") {
  logger.info("Deploying application commands...");
  await deploy();
} else {
  console.error('Invalid command! Please use either "start" or "deploy".');
}
