const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = 3003;

app.use(cors());
app.use(express.json());

app.post('/validate/hallucination', async (req, res) => {
  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'Text is required' });
  }
  try {
    const prompt = `Determine if the following statement contains hallucinations or unsupported claims. Provide a brief explanation if issues are found:\n\n"${text}"`;
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
    const isHallucinated = aiOutput.toLowerCase().includes("unsupported");
    res.json({
      type: "hallucination_check",
      valid: !isHallucinated,
      confidence: isHallucinated ? 0.5 : 0.95,
      issues: isHallucinated ? [aiOutput] : []
    });
  } catch (error) {
    console.error("Error in hallucination validator:", error.message);
    res.status(500).json({ error: "OpenAI API error in hallucination validator" });
  }
});

app.listen(PORT, () => {
  console.log(`Hallucination Validator running at http://localhost:${PORT}`);
});