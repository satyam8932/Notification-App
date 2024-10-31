// src/models/Subscription.ts
import { DataTypes, Model, Optional } from 'sequelize';
import sequelize from '../config/config';
import User from './User';

interface SubscriptionAttributes {
  id: number;
  userId: number;                       // Unique ID of the user
  stripeCustomerId: string;             // Stripe customer ID
  stripeSubscriptionId: string;         // Stripe subscription ID
  stripePriceId?: string | null;        // Stripe price ID for the subscription
  stripeCurrentPeriodEnd?: Date | null; // End date for the current subscription period
}

interface SubscriptionCreationAttributes extends Optional<SubscriptionAttributes, 'id'> {}

class Subscription extends Model<SubscriptionAttributes, SubscriptionCreationAttributes> implements SubscriptionAttributes {
  public id!: number;
  public userId!: number;
  public stripeCustomerId!: string;
  public stripeSubscriptionId!: string;
  public stripePriceId?: string | null;
  public stripeCurrentPeriodEnd?: Date | null;

  public readonly createdAt!: Date;
  public readonly updatedAt!: Date;
}

Subscription.init(
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
    stripeCustomerId: {
      type: DataTypes.STRING(256),
      allowNull: false,
      unique: true,
    },
    stripeSubscriptionId: {
      type: DataTypes.STRING(256),
      allowNull: false,
      unique: true,
    },
    stripePriceId: {
      type: DataTypes.STRING(256),
      allowNull: true,
    },
    stripeCurrentPeriodEnd: {
      type: DataTypes.DATE,
      allowNull: true,
    },
  },
  {
    sequelize,
    modelName: 'Subscription',
  }
);

// Define associations
User.hasOne(Subscription, { foreignKey: 'userId' });
Subscription.belongsTo(User, { foreignKey: 'userId' });

export default Subscription;
