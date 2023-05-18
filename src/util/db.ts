import { Dialect, Options, Sequelize } from "sequelize";
import config from "../config.js";

const sequelizeOptions: Options = {
  dialect: config.db.dialect as Dialect,
};

if (config.db.host) {
  sequelizeOptions.host = config.db.host;
}

if (config.db.port) {
  sequelizeOptions.port = config.db.port;
}

const db = new Sequelize(
  config.db.database,
  config.db.username,
  config.db.password,
  sequelizeOptions
);

export default db;
