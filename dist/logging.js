import config from "./config.js";
import winston from "winston";
// Define a log format with colors and timestamps
const alignedWithColorsAndTime = winston.format.combine(winston.format.colorize(), winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }), winston.format.align(), winston.format.printf((info) => `${info["timestamp"]} ${info.level}: ${info.message}`));
// Create a logger instance
const logger = winston.createLogger({
    levels: winston.config.syslog.levels,
});
// Check if console logging is enabled in the configuration
if (config.log.console.enabled) {
    // Add a console transport with the specified level or default level 'info'
    logger.add(new winston.transports.Console({
        format: alignedWithColorsAndTime,
        level: config.log.console.level,
    }));
}
// Check if file logging is enabled in the configuration
if (config.log.file.enabled) {
    // Add a file transport with the specified path or default path 'logs/tarubot.log'
    // and the specified level or the console level or default level 'info'
    logger.add(new winston.transports.File({
        filename: config.log.file.path,
        level: config.log.file.level ?? config.log.console.level ?? "info",
        format: winston.format.combine(winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }), winston.format.printf((info) => `${info["timestamp"]} ${info.level}: ${info.message}`)),
    }));
}
// Export the logger instance as the default export of the module
export default logger;
