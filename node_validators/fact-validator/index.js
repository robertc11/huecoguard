const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

app.post('/validate/fact', async (req, res) => {
  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'Text is required' });
  }
  try {
    const prompt = `Is the following statement factually accurate? Please provide a brief explanation if not:\n\n"${text}"`;
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.2
      },
      {
        headers: {
          "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );
    const aiOutput = response.data.choices[0].message.content;
    const isValid = !aiOutput.toLowerCase().includes("not accurate");
    const confidence = isValid ? 0.9 : 0.3;
    res.json({
      type: "fact_check",
      valid: isValid,
      confidence,
      issues: isValid ? [] : [aiOutput]
    });
  } catch (error) {
    console.error("Error in fact validator:", error.message);
    res.status(500).json({ error: "OpenAI API error in fact validator" });
  }
});

app.listen(PORT, () => {
  console.log(`Fact Validator running at http://localhost:${PORT}`);
});