require("dotenv").config();

const express = require("express");
const cors = require("cors");
const axios = require("axios");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const app = express();
app.use(cors());
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

app.post("/chat", async (req, res) => {
    const userMessage = req.body.message;

    try {
        const dashboard = await axios.get("http://127.0.0.1:8000/dashboard/");

        const context = `
        Income: ${dashboard.data.income}
        Expense: ${dashboard.data.expense}
        `;

        const model = genAI.getGenerativeModel({ model: "gemini-pro" });

        const result = await model.generateContent(
            context + "\nUser: " + userMessage
        );

        res.json({ reply: result.response.text() });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(5000, () => console.log("Chatbot running on port 5000"));