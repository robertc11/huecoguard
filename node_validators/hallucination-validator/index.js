require('dotenv').config(); // ✅ Load .env variables

const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { OpenAI } = require('openai');

const app = express();
const PORT = 3003;

app.use(cors());
app.use(express.json());

// ✅ Instantiate OpenAI with error check
if (!process.env.OPENAI_API_KEY) {
  console.error("❌ Missing OPENAI_API_KEY in environment variables.");
  process.exit(1);
}

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// ✅ Load grounded hallucination rules
const groundTruthsPath = path.resolve(__dirname, '../../autogen_core/policies/ground_truths.json');
const groundTruths = JSON.parse(fs.readFileSync(groundTruthsPath, 'utf-8'));
const rules = groundTruths.hallucination_rules || [];

console.log(`📘 Loaded ${rules.length} hallucination rules from: ${groundTruthsPath}`);

// ✅ Match regex-based hallucination rules
function checkAgainstRules(text, rules) {
  console.log("🔍 Checking text against hallucination rules...");
  return rules
    .filter(rule => new RegExp(rule.pattern, 'i').test(text))
    .map(rule => {
      console.log(`❗ Matched rule: ${rule.rule}`);
      return `${rule.rule}: ${rule.explanation}`;
    });
}

// ✅ Ask OpenAI for hallucination observation
async function getAgenticObservation(text) {
  console.log("🧠 Calling OpenAI for agentic observation...");

  const prompt = `You are validating whether a support assistant hallucinated a feature or capability of the CP2/KP2 SmartWitness camera system. Read the assistant's answer:\n\n"${text}"\n\nDoes it mention or imply a feature that is not actually available on the device? Reply with one sentence explaining the hallucination, or say "None found."`;

  try {
    const chat = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
    });

    const result = chat.choices[0].message.content.trim();
    console.log("✅ Agentic observation response:", result);
    return result;
  } catch (err) {
    console.error("🚨 OpenAI agentic prompt error:", err.message);
    return "⚠️ Error retrieving agentic observation";
  }
}

app.post('/validate/hallucination', async (req, res) => {
  const { text } = req.body;
  console.log(`\n📥 Incoming hallucination validation request:\n"${text}"`);

  if (!text) {
    console.warn("⚠️ No text provided.");
    return res.status(400).json({ error: 'Text is required' });
  }

  const issues = checkAgainstRules(text, rules);
  const agenticObservation = await getAgenticObservation(text);

  const result = {
    type: 'hallucination_check',
    valid: issues.length === 0,
    confidence: issues.length === 0 ? 0.95 : 0.5,
    issues,
    agentic_observation: agenticObservation,
  };

  console.log("📤 Final hallucination validation result:", result);
  res.json(result);
});

app.listen(PORT, () => {
  console.log(`✅ Agentic Hallucination Validator running at http://localhost:${PORT}`);
});