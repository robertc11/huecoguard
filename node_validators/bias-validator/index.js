require('dotenv').config(); // ✅ Load .env first

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');

const app = express();
const PORT = 3002;

app.use(cors());
app.use(express.json());

// ✅ Instantiate OpenAI with fallback check
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

if (!process.env.OPENAI_API_KEY) {
  console.error("❌ Missing OPENAI_API_KEY in environment variables.");
  process.exit(1);
}

// ✅ Load grounded bias rules
const groundTruthsPath = path.resolve(__dirname, '../../autogen_core/policies/ground_truths.json');
const groundTruths = JSON.parse(fs.readFileSync(groundTruthsPath, 'utf-8'));
const rules = groundTruths.bias_rules || [];

console.log(`📘 Loaded ${rules.length} bias rules from: ${groundTruthsPath}`);

// ✅ Match regex-based rules
function checkAgainstRules(text, rules) {
  console.log("🔍 Checking text against bias rules...");
  return rules
    .filter(rule => new RegExp(rule.pattern, 'i').test(text))
    .map(rule => {
      console.log(`❗ Matched rule: ${rule.rule}`);
      return `${rule.rule}: ${rule.explanation}`;
    });
}

// ✅ Agentic reasoning prompt
async function getAgenticObservation(text) {
  console.log("🧠 Calling OpenAI for agentic observation...");

  const prompt = `You're evaluating a support assistant's response for possible bias. Does this sound overconfident, dismissive, or risky in tone? Use the following text:\n\n"${text}"\n\nRespond with one short sentence. Be cautious but fair.`;

  try {
    const chat = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.4,
    });

    const result = chat.choices[0].message.content.trim();
    console.log("✅ Agentic observation response:", result);
    return result;
  } catch (err) {
    console.error("🚨 OpenAI agentic prompt error:", err.message);
    return "⚠️ Error retrieving agentic observation";
  }
}

app.post('/validate/bias', async (req, res) => {
  const { text } = req.body;
  console.log(`\n📥 Incoming validation request:\n"${text}"`);

  if (!text) {
    console.warn("⚠️ No text provided.");
    return res.status(400).json({ error: 'Text is required' });
  }

  const issues = checkAgainstRules(text, rules);
  const agenticObservation = await getAgenticObservation(text);

  const result = {
    type: 'bias_check',
    valid: issues.length === 0,
    confidence: issues.length === 0 ? 0.95 : 0.7,
    issues,
    agentic_observation: agenticObservation,
  };

  console.log("📤 Final bias validation result:", result);
  res.json(result);
});

app.listen(PORT, () => {
  console.log(`✅ Agentic Bias Validator running at http://localhost:${PORT}`);
});