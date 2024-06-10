import { NextFunction, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';

export const validateUserInput = [
  body('name').custom(value => /^[A-Za-z\s]+$/.test(value)).withMessage('Name is invalid'),
  body('email').isEmail().withMessage('Email is not valid'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),

  (req:Request, res:Response, next:NextFunction) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    next();
  }
];