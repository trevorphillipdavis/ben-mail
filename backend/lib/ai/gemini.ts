import { GoogleGenerativeAI } from "@google/generative-ai";
import type { ClassifiedMessage, EmailMetadata } from "../schema.js";
import { buildClassifierPrompt, parseClassifierJson } from "./classifier.js";

export async function classifyWithGemini(
  messages: EmailMetadata[],
): Promise<ClassifiedMessage[]> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is required when AI_PROVIDER=gemini");
  }

  const modelName = process.env.GEMINI_MODEL || "gemini-2.5-flash";
  const client = new GoogleGenerativeAI(apiKey);
  const model = client.getGenerativeModel({
    model: modelName,
    generationConfig: {
      responseMimeType: "application/json",
      temperature: 0,
    },
  });

  const result = await model.generateContent(buildClassifierPrompt(messages));
  const text = result.response.text();
  return parseClassifierJson(
    text,
    messages.map((message) => message.id),
  );
}
