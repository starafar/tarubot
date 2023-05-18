import { DataTypes, Model } from "sequelize";
import sequelize from "../util/db.js";
import User from "./user.js";
import SignUp from "./signup.js";

class Event extends Model {
  public id!: string;
  public name!: string;
  public description?: string;
  public startTime!: Date;
  public duration?: number;
}

Event.init(
  {
    id: {
      type: DataTypes.STRING,
      primaryKey: true,
      allowNull: false,
      unique: true,
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    description: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    startTime: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    duration: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
  },
  {
    sequelize,
    modelName: "Event",
  }
);

Event.belongsTo(User);
Event.hasMany(SignUp);

export default Event;
