import { DataTypes, Model } from "sequelize";
import sequelize from "../util/db.js";
import Character from "./character.js";
class Job extends Model {
    name;
    level;
}
Job.init({
    name: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: {
            isIn: [
                [
                    "Paladin",
                    "Warrior",
                    "Dark Knight",
                    "Gunbreaker",
                    "White Mage",
                    "Scholar",
                    "Astrologian",
                    "Sage",
                    "Monk",
                    "Dragoon",
                    "Ninja",
                    "Samurai",
                    "Reaper",
                    "Bard",
                    "Machinist",
                    "Dancer",
                    "Black Mage",
                    "Summoner",
                    "Red Mage",
                    "Blue Mage",
                ],
            ],
        },
    },
    level: {
        type: DataTypes.INTEGER,
        allowNull: false,
        validate: {
            min: 1,
            max: 90,
        },
    },
}, {
    sequelize,
    modelName: "Job",
});
Job.belongsTo(Character);
export default Job;
