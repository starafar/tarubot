import { Sequelize } from "sequelize";
import config from "config";
const dbConfig = config.get("db");
const db = new Sequelize(dbConfig.database, dbConfig.username, dbConfig.password, {
    host: dbConfig.host,
    dialect: dbConfig.dialect,
});
export default db;
