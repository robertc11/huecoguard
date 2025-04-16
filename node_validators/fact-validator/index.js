// const express = require('express');
// const axios = require('axios');
// const cors = require('cors');
// require('dotenv').config();

// const app = express();
// const PORT = 3001;

// app.use(cors());
// app.use(express.json());

// app.post('/validate/fact', async (req, res) => {
//   const { text } = req.body;
//   if (!text) {
//     return res.status(400).json({ error: 'Text is required' });
//   }
//   try {
//     const prompt = `Is the following statement factually accurate? Please provide a brief explanation if not:\n\n"${text}"`;
//     const response = await axios.post(
//       'https://api.openai.com/v1/chat/completions',
//       {
//         model: "gpt-3.5-turbo",
//         messages: [{ role: "user", content: prompt }],
//         temperature: 0.2
//       },
//       {
//         headers: {
//           "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
//           "Content-Type": "application/json"
//         }
//       }
//     );
//     const aiOutput = response.data.choices[0].message.content;
//     const isValid = !aiOutput.toLowerCase().includes("not accurate");
//     const confidence = isValid ? 0.9 : 0.3;
//     res.json({
//       type: "fact_check",
//       valid: isValid,
//       confidence,
//       issues: isValid ? [] : [aiOutput]
//     });
//   } catch (error) {
//     console.error("Error in fact validator:", error.message);
//     res.status(500).json({ error: "OpenAI API error in fact validator" });
//   }
// });

// app.listen(PORT, () => {
//   console.log(`Fact Validator running at http://localhost:${PORT}`);
// });
// const express = require('express');
// const cors = require('cors');
// const fs = require('fs');
// const path = require('path');

// const app = express();
// const PORT = 3001;

// app.use(cors());
// app.use(express.json());

// // ✅ Load grounded fact rules from correct path
// const groundTruthsPath = path.resolve(__dirname, '../../autogen_core/policies/ground_truths.json');
// const groundTruths = JSON.parse(fs.readFileSync(groundTruthsPath, 'utf-8'));
// const rules = groundTruths.fact_rules || [];

// // ✅ Match input text against grounded rule patterns
// function checkAgainstRules(text, rules) {
//   return rules
//     .filter(rule => new RegExp(rule.pattern, 'i').test(text))
//     .map(rule => `${rule.rule}: ${rule.explanation}`);
// }

// app.post('/validate/fact', (req, res) => {
//   const { text } = req.body;
//   if (!text) return res.status(400).json({ error: 'Text is required' });

//   const issues = checkAgainstRules(text, rules);

//   res.json({
//     type: 'fact_check',
//     valid: issues.length === 0,
//     confidence: issues.length === 0 ? 0.95 : 0.3,
//     issues
//   });
// });

// app.listen(PORT, () => {
//   console.log(`✅ Fact Validator running at http://localhost:${PORT}`);
// });
require('dotenv').config(); // ✅ Load .env variables

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

if (!process.env.OPENAI_API_KEY) {
  console.error("❌ Missing OPENAI_API_KEY in environment variables.");
  process.exit(1);
}

// ✅ Load grounded fact rules
const groundTruthsPath = path.resolve(__dirname, '../../autogen_core/policies/ground_truths.json');
const groundTruths = JSON.parse(fs.readFileSync(groundTruthsPath, 'utf-8'));
const rules = groundTruths.fact_rules || [];

// ✅ Match regex-based rules
function checkAgainstRules(text, rules) {
  console.log("🔍 Running regex-based rule checks...");
  return rules
    .filter(rule => new RegExp(rule.pattern, 'i').test(text))
    .map(rule => `${rule.rule}: ${rule.explanation}`);
}

// ✅ Agentic prompt for evaluating factual accuracy
async function getAgenticObservation(text) {
  const prompt = `You're validating a support assistant's answer for factual accuracy regarding camera system installation, LED behavior, and device usage. Read the following statement:\n\n"${text}"\n\nDoes anything appear to be factually incorrect or contradict common safety practices or device manuals (CP2, KP2, SmartWitness)? Reply with a short sentence and be specific.`;

  console.log("🧠 Sending to OpenAI for agentic observation...");
  const chat = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.3,
  });

  const reply = chat.choices[0].message.content.trim();
  console.log("💬 Agentic observation received:", reply);
  return reply;
}

app.post('/validate/fact', async (req, res) => {
  const { text } = req.body;
  if (!text) {
    console.warn("⚠️ No text provided to /validate/fact");
    return res.status(400).json({ error: 'Text is required' });
  }

  console.log("📥 Received text:", text);

  const issues = checkAgainstRules(text, rules);
  const agenticObservation = await getAgenticObservation(text);

  const result = {
    type: 'fact_check',
    valid: issues.length === 0,
    confidence: issues.length === 0 ? 0.95 : 0.3,
    issues,
    agentic_observation: agenticObservation,
  };

  console.log("✅ Fact check result:", result);

  res.json(result);
});

app.listen(PORT, () => {
  console.log(`✅ Agentic Fact Validator running at http://localhost:${PORT}`);
});