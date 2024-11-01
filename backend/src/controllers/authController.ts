import { Request, Response } from 'express';
import User from '../models/User';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

export const registerUser = async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, username, password } = req.body;

    // Check if email is already taken
    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      res.status(400).json({ message: 'Email already in use' });
      return;
    }

    // Hash password and create new user
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = await User.create({ email, username, password: hashedPassword });
    
    res.status(201).json({ message: 'User registered successfully', user: { id: newUser.id, email: newUser.email, username: newUser.username } });
  } catch (error: unknown) {
    const err = error as Error;
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

export const loginUser = async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password } = req.body;

    // Find user by email
    const user = await User.findOne({ where: { email } });
    if (!user) {
      res.status(401).json({ message: 'Invalid credentials' });
      return;
    }

    // Verify password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      res.status(401).json({ message: 'Invalid credentials' });
      return;
    }

    // Generate JWT
    const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET as string, {
      expiresIn: '1h',
    });

    res.json({ message: 'Login successful', token });
  } catch (error: unknown) {
    const err = error as Error;
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};
