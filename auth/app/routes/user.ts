//user routes
import express, { Request, Response } from 'express';
import User from '../models/user';
import { validateUserInput } from '../middlewares/validation';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import authenticate from '../middlewares/authenticate';
import { RequestWithUser } from '../interfaces/IUser';
// import client from '../../redis';
// import checkCache from '../middlewares/cache';
// import tokenCache from '../middlewares/tokenCache';
import loginLimiter from '../middlewares/loginLimiter';
import { sendMail } from '../services/mailer';
import crypto from 'crypto';
import { validateResetPassword } from '../middlewares/inputResetValidation';
import passport from 'passport';
import isVerified from '../middlewares/isVerified';
const router = express.Router();


//implementing refresh token rotation strategy  
//PUT /users/refresh-token
router.put('/refresh-token', async (req: RequestWithUser, res: Response) => {
    try {
        const refreshToken = req.body.refresh_token;
        if (!refreshToken) return res.status(401).json({ error: 'Refresh token is required' });
        try{
            const user =  jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET as string) as jwt.JwtPayload;
            res.status(200).json({ access_token: jwt.sign({ email: user?.email, id: user?.id }, process.env.JWT_SECRET as string, { expiresIn: '10m' }) });
        }
        catch(err){
            return res.status(401).json({ error: 'Refresh token is invalid' });
        }
    }
    catch (error: any) {
        res.status(500).json({ error: error.message });
    }
}
);

//signup route 
//POST /users/signup
router.post('/signup', validateUserInput, async (req: Request, res: Response) => {
    try {
        const {
            name,
            email,
            password,
        } = req.body;

        //check if user already exists
        const userExists = await User.findOne({ email });
        if (userExists) return res.status(400).json({ error: 'User already exists' });

        //encrypt password
        const salt = await bcrypt.genSalt(Number(process.env.SALT));
        const hashedPassword = await bcrypt.hash(password, salt);

        //send email verification
        const data = { name, email, password: hashedPassword, verified: false}
        const newUser = new User(data);
        const isSent = await sendMail(data.email);
        if (!isSent) return res.status(500).json({ error: 'Error sending verification email' });
        await newUser.save();

        //generate token
        let access_token = jwt.sign({ email: newUser.email, id: newUser._id }, process.env.JWT_SECRET as string, { expiresIn: '24h' });
        let refresh_token = jwt.sign({ email: newUser.email, id: newUser._id }, process.env.REFRESH_TOKEN_SECRET as string, { expiresIn: '7d' });
        // client.setex(refresh_token, 604800, JSON.stringify({ refresh_token: refresh_token }));
        res.status(201).json(
            {
                message: 'User created successfully',
                access_token: access_token,
                refresh_token: refresh_token
            });
    }
    catch (error: any) {
        res.status(500).json({ error: error.message });
    }
}
);

//verification route
//GET /users/verify/:token
router.get('/verify/:token', async (req: Request, res: Response) => {
    try {
        const token = req.params.token;
        const decoded = jwt.verify(token, process.env.VERIFICATION_SECRET as string) as jwt.JwtPayload;
        if (!decoded) return res.status(400).json({ error: 'Invalid token' });
        const user = await User.findOne({ email: decoded.email });
        if (!user) return res.status(400).json({ error: 'User not found' });
        user.verified = true;
        await user.save();
        res.status(200).json({ message: 'Email verified' });
    }
    catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});

//login route 
//POST /users/login
router.post('/login', async (req: Request, res: Response) => {
    try {
        const { email, password } = req.body;

        //check if user exists and the credentials are valid
        const user = await User.findOne({ email })
        const validPassword = await bcrypt.compare(password, user?.password ?? '');
        if (!validPassword || !user) return res.status(401).json({ error: 'Invalid credentials' });

        //generate token if valid so that the token can be stored in session/local storage
        const access_token = jwt.sign({ email: user.email, id: user._id }, process.env.JWT_SECRET as string, { expiresIn: '24h' })
        const refresh_token = jwt.sign({ email: user.email, id: user._id }, process.env.REFRESH_TOKEN_SECRET as string, { expiresIn: '7d' })
        // client.setex(refresh_token, 604800, JSON.stringify({ refresh_token: refresh_token }));
        res.status(200).json(
            {
                message: 'Login successful',
                access_token: access_token,
                refresh_token: refresh_token

            });
    }
    catch (error: any) {
        res.status(500).json({ error: error.message });
    }
});


//GET /users
router.get('/', authenticate, async (req: RequestWithUser, res: Response) => {
    try {
        const user = await User.findById(req.user?.id);
        if (!user) return res.status(400).json({ error: 'User not found' });
        // client.setex(req.user?.id, 3600, JSON.stringify({ name: user.name, email: user.email, phone: user.phone, gender: user.gender }));
        res.status(200).json({name: user.name, email: user.email, phone: user.phone, gender: user.gender})
    }
    catch(err:any){
        res.status(500).json({ error: err.message });
    }
});

//PUT /users
router.put('/', authenticate, isVerified, validateUserInput, async (req: RequestWithUser, res: Response) => {
    try {
        const user = await User.findById(req.user?.id);
        if (!user) return res.status(400).json({ error: 'User not found' });
        const { name, email, gender, phone } = req.body;
        user.name = name;
        user.email = email;
        user.gender = gender;
        user.phone = phone;
        await user.save();
        res.status(200).json({ message: 'User updated successfully' });
    }
    catch (err: any) {
        res.status(500).json({ error: err.message });
    
    }
});

//logout route
//DELETE /users/logout
// router.delete('/logout', authenticate, async (req: Request, res: Response) => {
//     try {
//         client.del(req.body.refresh_token, (err, reply) => {
//             if(err) res.status(500).json({ error: err.message });
//             res.status(200).json({ message: 'User logged out successfully' });
//         });
//     }
//     catch(err:any){
//         res.status(500).json({ error: err.message });
//     }
// });

//reset password
//POST /users/forgot-password
router.post('/forgot-password', async (req: Request, res: Response) => {
    try {
        const email = req.body.email;
        const user = await User.findOne(email);
        if (!user) return res.status(400).json({ error: 'User not found' });

        //generate token and make sure its single use
        const resetToken = crypto.randomBytes(64).toString('hex');
        // client.del(`reset:${email}`); //make sure there is no duplicate token
        // client.setex(`reset:${email}`, 600, resetToken);
        const isSent = await sendMail(email, resetToken);
        if (!isSent) return res.status(500).json({ error: 'Error sending reset email' });
        res.status(200).json({ message: 'Reset email sent' });
    }
    catch(err:any){
        res.status(500).json({ error: err.message });
    }
});

//PUT /users/reset-password
router.put('/reset-password', validateResetPassword, async (req: Request, res: Response) => {
    try {
        const { resetToken, token } = req.query;
        const { password } = req.body;
        const email = jwt.verify(token as string, process.env.VERIFICATION_SECRET as string) as jwt.JwtPayload;
        // const isValid = await client.get(`reset:${email}`);
        // if (isValid !== resetToken) return res.status(400).json({ error: 'Invalid token' });

        //encrypt password
        const salt = await bcrypt.genSalt(Number(process.env.SALT));
        const hashedPassword = await bcrypt.hash(password, salt);
        const user = await User.findOne(email)
        if (!user) return res.status(400).json({ error: 'User not found' });
        user.password = hashedPassword;
        await user.save();
        
        res.status(200).json({ message: 'Password reset successful' });
    }
    catch(err:any){
        res.status(500).json({ error: err.message });
    }
});

//POST /users/set-password
router.post('/set-password', authenticate, validateResetPassword, async (req: RequestWithUser, res: Response) => {
    try {
        const { password } = req.body;
        const user = await User.findById(req.user?.id);
        if (!user) return res.status(400).json({ error: 'User not found' });
        if(user.password) return res.status(400).json({ error: 'Password already set' });

        //encrypt password
        const salt = await bcrypt.genSalt(Number(process.env.SALT));
        const hashedPassword = await bcrypt.hash(password, salt);
        user.password = hashedPassword;
        await user.save();
        res.status(200).json({ message: 'Password reset successful' });
    }
    catch(err:any){
        res.status(500).json({ error: err.message });
    }
});

//PUT /users/new-password
router.put('/new-password', authenticate, validateResetPassword, loginLimiter, async (req: RequestWithUser, res: Response) => {
    try {
        const { password, previousPassword } = req.body;
        const user = await User.findById(req.user?.id);
        if (!user) return res.status(400).json({ error: 'User not found' });
        const validPassword = await bcrypt.compare(previousPassword, user.password as string);
        if (!validPassword) return res.status(400).json({ error: 'Previous password is incorrect' });
        const samePassword = await bcrypt.compare(password, user.password as string);
        if (samePassword) return res.status(400).json({ error: 'New password cannot be the same as the previous password' });

        //encrypt password
        const salt = await bcrypt.genSalt(Number(process.env.SALT));
        const hashedPassword = await bcrypt.hash(password, salt);
        user.password = hashedPassword;
        await user.save();
        res.status(200).json({ message: 'Password reset successful' });
    }
    catch(err:any){
        res.status(500).json({ error: err.message });
    }
});


//GET /users/auth/google
router.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

//GET /users/auth/google/callback
router.get('/auth/google/callback', passport.authenticate('google', { failureRedirect: '/login', session: false }), (req:RequestWithUser, res:Response) => {
    // client.setex(req.user?.refresh_token, 604800, JSON.stringify({ refresh_token: req.user?.refresh_token }));
    res.status(200).json({ message: 'Login successful', access_token: req.user?.access_token, refresh_token: req.user?.refresh_token});
});



export default router;