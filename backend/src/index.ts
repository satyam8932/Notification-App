import express, { Request, Response } from 'express';
import sequelize from './config/config';
import User from './models/User';
import Subscription from './models/Subscription';
import Filter from './models/Filter';
import Notification from './models/Notification';
import authRoutes from './routes/authRoutes';
import dotenv from 'dotenv';
import listEndpoints from 'express-list-endpoints';
dotenv.config();

const app = express();

// Middleware to parse JSON request bodies
app.use(express.json());

// Initialize the model schema (ensures the models are loaded)
User;
Subscription;
Filter;
Notification;

// Basic route for testing
app.get('/', (req: Request, res: Response) => {
  res.send('Welcome to the Backend!');
});

// Register routes
app.use('/api/auth', authRoutes);

// PORT Define
const PORT = process.env.PORT || 5000;

// Sync Sequelize models and start the server
sequelize.sync()
  .then(() => {
    app.listen(PORT, () => {
      console.log('Server running on port 5000');

      // Display all endpoints
      const endpoints = listEndpoints(app);
      endpoints.forEach((endpoint) => {
        console.log(`${endpoint.methods.join(', ')} ${endpoint.path}`);
      });
    });
  })
  .catch((err: Error) => {
    console.error('Unable to connect to the database:', err);
  });
