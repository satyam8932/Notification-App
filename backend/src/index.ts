import express from 'express';
import sequelize from './config/config';
import User from './models/User';
import Subscription from './models/Subscription';
import Filter from './models/Filter';
import Notification from './models/Notification';

const app = express();

// Middleware to parse JSON request bodies
app.use(express.json());

// Initialize the model schema
User;
Subscription;
Filter;
Notification;

// Basic route for testing
app.get('/', (req, res) => {
  res.send('Welcome to the server!');
});

// Route to handle incoming notifications
app.post('/notification', (req, res) => {
  const notificationData = req.body;
  console.log('Received notification:', notificationData);

  // You can add further processing here, such as saving to the database or handling the notification data as needed.

  // Send a response back to the sender
  res.status(200).json({ message: 'Notification received successfully' });
});

// Sync Sequelize models and start the server
sequelize.sync().then(() => {
  app.listen(5000, () => {
    console.log('Server running on port 5000');
  });
}).catch(err => console.error('Unable to connect to the database:', err));
