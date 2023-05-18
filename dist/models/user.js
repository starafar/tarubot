import { DataTypes, Model } from "sequelize";
import sequelize from "../util/db.js";
class User extends Model {
    username;
}
User.init({
    username: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
    },
}, {
    sequelize,
    modelName: "User",
});
export default User;
