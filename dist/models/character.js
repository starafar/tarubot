import { DataTypes, Model } from "sequelize";
import sequelize from "../util/db.js";
import User from "./user.js";
import Job from "./job.js";
import SignUp from "./signup.js";
class Character extends Model {
    id;
}
Character.init({
    name: {
        type: DataTypes.BIGINT,
        allowNull: false,
    },
}, {
    sequelize,
    modelName: "Character",
});
Character.belongsTo(User);
Character.hasMany(Job);
Character.hasMany(SignUp);
export default Character;
