const express = require('express');
const bodyParser = require('body-parser');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Increase limit for base64 image data
app.use(bodyParser.json({ limit: '50mb' }));

// Load Config
const configPath = path.join(__dirname, 'brain_config.json');
let config = {};
try {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) {
    console.error("Error loading config:", e);
}

const API_KEY = config.api_keys?.gemini || "";
const genAI = new GoogleGenerativeAI(API_KEY);

// Model Selection
// User requested: gemini-2.5-flash-native-audio-dialog (Live API)
// But for REST API (Screenshots), we use the latest Flash model.
// We will try to use 'gemini-2.0-flash-exp' as a safe default for free/experimental usage.
const MODEL_NAME = 'gemini-2.0-flash-exp'; 

console.log(`>>> Gongmyung AI Node Server Initialized <<<`);
console.log(`- Model: ${MODEL_NAME}`);
console.log(`- API Key: ${API_KEY ? "Loaded" : "Missing"}`);

app.post('/analyze', async (req, res) => {
    try {
        const { prompt, image, metrics } = req.body;

        if (!API_KEY) {
            return res.json({ answer: "API Key Missing" });
        }

        const model = genAI.getGenerativeModel({ model: MODEL_NAME });

        // Prepare content
        const parts = [];
        
        // Add text prompt
        parts.push({ text: prompt });

        // Add image if provided (base64)
        if (image) {
            parts.push({
                inlineData: {
                    mimeType: "image/png",
                    data: image
                }
            });
        }

        const result = await model.generateContent(parts);
        const response = await result.response;
        const text = response.text();

        console.log(`[AI Server] 💡 Answer: ${text}`);
        res.json({ answer: text });

    } catch (error) {
        console.error("[AI Server] ❌ Error:", error.message);
        res.json({ answer: `Error: ${error.message}` });
    }
});

app.listen(PORT, () => {
    console.log(`[AI Server] Listening on port ${PORT}`);
});
