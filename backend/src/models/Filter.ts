// src/models/Filter.ts
import { DataTypes, Model, Optional } from 'sequelize';
import sequelize from '../config/config';
import User from './User';

interface FilterAttributes {
  id: number;
  userId: number;
  notificationType: string;
  brand: string;
  model: string;
  yearStart: string;
  yearEnd: string;
  fuelType: string;
  transmission: string;
  priceFrom: string;
  priceTo: string;
  color: string;
  bodyType: string;
  origin: string;
  pageUrl: string;
  currentVehicleCount: number;
}

interface FilterCreationAttributes extends Optional<FilterAttributes, 'id'> {}

class Filter extends Model<FilterAttributes, FilterCreationAttributes> implements FilterAttributes {
  public id!: number;
  public userId!: number;
  public notificationType!: string;
  public brand!: string;
  public model!: string;
  public yearStart!: string;
  public yearEnd!: string;
  public fuelType!: string;
  public transmission!: string;
  public priceFrom!: string;
  public priceTo!: string;
  public color!: string;
  public bodyType!: string;
  public origin!: string;
  public pageUrl!: string;
  public currentVehicleCount!: number;

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
    notificationType: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    brand: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    model: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    yearStart: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    yearEnd: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    fuelType: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    transmission: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    priceFrom: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    priceTo: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    color: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    bodyType: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    origin: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    pageUrl: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    currentVehicleCount: {
      type: DataTypes.INTEGER,
      allowNull: true,
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
