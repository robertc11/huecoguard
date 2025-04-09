const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = 3002;

app.use(cors());
app.use(express.json());

app.post('/validate/bias', async (req, res) => {
  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'Text is required' });
  }
  try {
    const prompt = `Analyze the following text for potential bias and provide a concise summary:\n\n"${text}"`;
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.3
      },
      {
        headers: {
          "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );
    const aiOutput = response.data.choices[0].message.content;
    const hasBias = aiOutput.toLowerCase().trim() !== "";
    res.json({
      type: "bias_check",
      valid: !hasBias,
      confidence: hasBias ? 0.7 : 0.95,
      issues: hasBias ? [aiOutput] : []
    });
  } catch (error) {
    console.error("Error in bias validator:", error.message);
    res.status(500).json({ error: "OpenAI API error in bias validator" });
  }
});

app.listen(PORT, () => {
  console.log(`Bias Validator running at http://localhost:${PORT}`);
});