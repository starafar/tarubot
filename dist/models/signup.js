import { DataTypes, Model } from "sequelize";
import sequelize from "../util/db.js";
import Event from "./event.js";
import Character from "./character.js";
import Job from "./job.js";
class SignUp extends Model {
}
SignUp.init({
    eventId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Event,
            key: "id",
        },
    },
    characterId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: Character,
            key: "id",
        },
    },
    jobName: {
        type: DataTypes.STRING,
        allowNull: false,
        references: {
            model: Job,
            key: "name",
        },
    },
}, {
    sequelize,
    modelName: "SignUp",
});
SignUp.belongsTo(Event, { foreignKey: "eventId" });
SignUp.hasMany(Character, { foreignKey: "characterId" });
SignUp.hasMany(Job, { foreignKey: "jobName" });
export default SignUp;
