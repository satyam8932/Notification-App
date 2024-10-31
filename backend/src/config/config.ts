import { Sequelize } from 'sequelize';
import dotenv from 'dotenv';

dotenv.config();

let sequelize: Sequelize;

try {
  sequelize = new Sequelize(process.env.DATABASE_URL || '', {
    dialect: 'postgres',
    logging: false,
  });

  // Test the connection to ensure it works
  sequelize.authenticate()
    .then(() => {
      console.log('Database connection has been established successfully.');
    })
    .catch((err) => {
      console.error('Unable to connect to the database:', err);
      process.exit(1); // Exit the process to let Nodemon restart the app
    });
} catch (error) {
  console.error('Error while setting up the database:', error);
  process.exit(1); // Exit the process to let Nodemon restart the app
}

export default sequelize;
