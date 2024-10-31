// src/models/Filter.ts
import { DataTypes, Model, Optional } from 'sequelize';
import sequelize from '../config/config';
import User from './User';

interface FilterAttributes {
  id: number;
  userId: number;
  brand: string;
  model: string;
  yearStart: number;
  yearEnd: number;
  fuelType: string;
  transmission: string;
}

interface FilterCreationAttributes extends Optional<FilterAttributes, 'id'> {}

class Filter extends Model<FilterAttributes, FilterCreationAttributes> implements FilterAttributes {
  public id!: number;
  public userId!: number;
  public brand!: string;
  public model!: string;
  public yearStart!: number;
  public yearEnd!: number;
  public fuelType!: string;
  public transmission!: string;

  public readonly createdAt!: Date;
  public readonly updatedAt!: Date;
}

Filter.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    userId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      references: {
        model: User,
        key: 'id',
      },
      onDelete: 'CASCADE',
      onUpdate: 'CASCADE',
    },
    brand: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    model: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    yearStart: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    yearEnd: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    fuelType: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    transmission: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  },
  {
    sequelize,
    modelName: 'Filter',
  }
);

// Define associations
User.hasMany(Filter, { foreignKey: 'userId' });
Filter.belongsTo(User, { foreignKey: 'userId' });

export default Filter;
