import config from "config";
import winston from "winston";

// Define a log format with colors and timestamps
const alignedWithColorsAndTime = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
  winston.format.align(),
  winston.format.printf(
    (info) => `${info["timestamp"]} ${info.level}: ${info.message}`
  )
);

// Create a logger instance
const logger = winston.createLogger({
  levels: winston.config.syslog.levels,
});

// Check if console logging is enabled in the configuration
if (config.get("log.console.enabled")) {
  // Add a console transport with the specified level or default level 'info'
  logger.add(
    new winston.transports.Console({
      format: alignedWithColorsAndTime,
      level: config.get("log.console.level") || "info",
    })
  );
}

// Check if file logging is enabled in the configuration
if (config.get("log.file.enabled")) {
  // Add a file transport with the specified path or default path 'logs/tarubot.log'
  // and the specified level or the console level or default level 'info'
  logger.add(
    new winston.transports.File({
      filename: config.get("log.file.path") ?? "logs/tarubot.log",
      level:
        config.get("log.file.level") ||
        (config.get("log.console.enabled")
          ? config.get("log.console.level") || "info"
          : "info"),
      format: winston.format.combine(
        winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
        winston.format.printf(
          (info) => `${info["timestamp"]} ${info.level}: ${info.message}`
        )
      ),
    })
  );
}

// Check if no transports are configured.
if (!logger.transports) {
  // Add a console transport with level 'info'
  logger.add(
    new winston.transports.Console({
      format: alignedWithColorsAndTime,
      level: "info",
    })
  );

  // Log a warning message
  logger.warning(
    "No logging configuration found in config/local.yaml. Logging to console with level 'info'."
  );
}
// Export the logger instance as the default export of the module
export default logger;
