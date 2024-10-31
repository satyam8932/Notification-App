import express from 'express';
import sequelize from './config/config';
import User from './models/User';
import Subscription from './models/Subscription';
import Filter from './models/Filter';
import Notification from './models/Notification';

const app = express();

// Initialize the model schema
User;
Subscription;
Filter;
Notification;

// Basic route for testing
app.get('/', (req, res) => {
  res.send('Welcome to the server!');
});

// Sync Sequelize models and start the server
sequelize.sync().then(() => {
  app.listen(5000, () => {
    console.log('Server running on port 5000');
  });
}).catch(err => console.error('Unable to connect to the database:', err));
