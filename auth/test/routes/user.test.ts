import redisMock from "redis-mock";
import request from "supertest";
import express from "express";
import userRouter from "../../app/routes/user";
import mongoose from "mongoose";
import dotenv from "dotenv";
import { MongoMemoryServer } from "mongodb-memory-server";
import sinon from "sinon";
// import client from "../../redis";
import { sendMail } from "../../app/services/mailer";

dotenv.config({ path: ".env.test.local" });
const app = express();
app.use(express.json());
app.use("/users", userRouter);

jest.mock("../../app/services/mailer", ()=>({
    sendMail: jest.fn(),
}));

// jest.mock("../../redis", () => {
//     return redisMock.createClient();
// });

const mockedSendMail = sendMail as jest.MockedFunction<typeof sendMail>

let mongoServer: any;
let clock: sinon.SinonFakeTimers;
describe("User routes", () => {

    beforeAll(async () => {
        mongoServer = await MongoMemoryServer.create();
        const mongoUri = mongoServer.getUri();
        await mongoose.connect(mongoUri);
    });

    beforeEach(async () => {
        clock = sinon.useFakeTimers({ shouldClearNativeTimers: true })
    });

    afterEach(async () => {
        clock.restore();
    });

    afterAll(async () => {
        await mongoose.connection.dropDatabase();
        await mongoose.connection.close();
        await mongoServer.stop();
        // client.flushdb();
        // client.quit();
    });

    let access_token: string;
    let refresh_token: string;

    it("should create a new user", async () => {
        mockedSendMail.mockResolvedValue(true)
        const res = await request(app)
            .post("/users/signup")
            .send({
                name: "John Doe",
                email: "john@mail.com",
                phone: "08212345678",
                password: "password",
                gender: "Male"
            });
        expect(mockedSendMail).toHaveBeenCalledWith("john@mail.com")
        expect(res.status).toEqual(201);
        expect(res.body).toHaveProperty("message");
        expect(res.body).toHaveProperty("access_token");
        expect(res.body).toHaveProperty("refresh_token");
        access_token = res.body.access_token;
        refresh_token = res.body.refresh_token;
    }, 5000);

    it("should invalidate a user input", async () => {
        const res = await request(app)
            .post("/users/signup")
            .send({
                name: "John123",
                email: "xana",
                phone: "02212345678",
                password: "pasord",
                gender: "ale"
            });
        expect(res.status).toEqual(400);
        expect(res.body).toHaveProperty("errors");
        const validPaths = ["name", "email", "phone", "password", "gender"];
        res.body.errors.forEach((error: any) => {
            expect(validPaths).toContain(error.path);
        });
    }, 5000);

    it("should login a user", async () => {
        const res = await request(app)
            .post("/users/login")
            .send({
                email: "john@mail.com",
                password: "password",
            });
        expect(res.status).toEqual(200);
        expect(res.body).toHaveProperty("access_token");
        expect(res.body).toHaveProperty("refresh_token");
        access_token = res.body.access_token;
        refresh_token = res.body.refresh_token;
    }, 5000);

    it("should not let user log in due to invalid credentials", async () => {
        const res = await request(app)
            .post("/users/login")
            .send({
                email: "adam@mail.com",
                password: "password",
            });
        expect(res.status).toEqual(401);
        expect(res.body).toHaveProperty("error");
    }, 5000);

    it("should not let user log in due to too many requests", async () => {
        for (let i = 0; i < 10; i++) {
            await request(app)
                .post("/users/login")
                .send({
                    email: "ngarang@mail.com",
                    password: "password",
                });
        }
        const res = await request(app)
            .post("/users/login")
            .send({
                email: "ngarang@mail.com",
                password: "password",
            });
        expect(res.status).toEqual(429);
        expect(res.body).toHaveProperty("error");
    }, 5000);

    it("should get the authenticated user data", async () => {
        let res = await request(app)
            .get("/users")
            .set("Authorization", `Bearer ${access_token}`);
        expect(res.status).toEqual(200);
        expect(res.body).toHaveProperty("name");
        expect(res.body).toHaveProperty("email");
        expect(res.body).toHaveProperty("phone");
        expect(res.body).toHaveProperty("gender");
    }, 6000);

    // it("should get the cache of user data", async () => {
    //     const res = await request(app)
    //         .get("/users")
    //         .set("Authorization", `Bearer ${access_token}`)

    //     expect(res.headers['x-cache-hit']).toEqual('true')
    //     expect(res.status).toEqual(200);
    //     expect(res.body).toHaveProperty("name");
    //     expect(res.body).toHaveProperty("email");
    //     expect(res.body).toHaveProperty("phone");
    // }, 5000);

    it("should invalidate access token", async () => {
        const res = await request(app)
            .get("/users")
            .set("Authorization", `Bearer invalid_token`);
        expect(res.status).toEqual(401);
        expect(res.body).toHaveProperty("error");
    }, 5000);

    it("should invalidate access token due to time", async () => {
        clock.tick(600000);
        const res = await request(app)
            .get("/users")
            .set("Authorization", `Bearer ${access_token}`);
        expect(res.status).toEqual(401);
        expect(res.body).toHaveProperty("error");
    }, 5000);

    it("should refresh the token", async () => {
        const res = await request(app)
            .put("/users/refresh-token")
            .send({ refresh_token });
        expect(res.status).toEqual(200);
        expect(res.body).toHaveProperty("access_token");
        access_token = res.body.access_token;
    }, 5000);

    it("should not refresh the token", async () => {
        const res = await request(app)
            .put("/users/refresh-token")
            .send({ refresh_token: "invalid_token" });
        expect(res.status).toEqual(401);
        expect(res.body).toHaveProperty("error");
    }, 5000);

    it("should not refresh the token due to time", async () => {
        clock.tick(604800000);
        const res = await request(app)
            .put("/users/refresh-token")
            .send({ refresh_token });
        expect(res.status).toEqual(401);
        expect(res.body).toHaveProperty("error");
    }, 5000);
    // it("should logout the user", async () => {
    //     const res = await request(app)
    //         .delete("/users/logout")
    //         .set("Authorization", `Bearer ${access_token}`)
    //         .send({ refresh_token });
    //     expect(res.status).toEqual(200);
    //     expect(res.body).toHaveProperty("message");
    // }, 5000);

});

