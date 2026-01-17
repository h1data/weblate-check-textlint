import express from "express";
import fs from "fs";
import path from "path";
import { createLinter, loadTextlintrc } from "textlint";

const app = express();
app.use(express.json({ limit: "2mb" }));

const CONFIG_ROOT = process.env.TEXTLINTRC_PATH || "/app/textlint";
const TARGET_LANGS = (process.env.TEXTLINT_LANGS || "ja").split(",");
const CONFIGURATIONS = new Map();
TARGET_LANGS.forEach(lang => { CONFIGURATIONS.set(lang, path.join(CONFIG_ROOT, `${lang}/.textlintrc`)); });

app.post(process.env.TEXTLINT_PATH || "/lint", async (req, res) => {
  try {
    const { text: text, lang: lang } = req.body || {};
    if (!text) {
      return res.status(400).json({ error: "Missing 'text'" });
    }

    const configPath = CONFIGURATIONS.get(lang);
    if (!configPath) {
      return res.json([""]);
    }

    // SECURITY: prevent directory traversal
    if (!configPath.startsWith(CONFIG_ROOT)) {
      throw new Error(`invalid config path: ${configPath}`);
    }

    if (!fs.existsSync(configPath)) {
      throw new Error(`config file not found: ${configPath}`);
    }

    const descriptor = await loadTextlintrc({ configFilePath: configPath });
    const linter = await createLinter({ descriptor });
    const result = await linter.lintText(text, "input.md");
    res.json(result);

  } catch (err) {
    console.error("[textlint-server] Error:", err);
    res.status(500);
  }

});

const PORT = process.env.TEXTLINT_PORT ? Number(process.env.TEXTLINT_PORT) : 3000;
app.listen(PORT, () => console.log(`textlint-server running on port ${PORT}`));
