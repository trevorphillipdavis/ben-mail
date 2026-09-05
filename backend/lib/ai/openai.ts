import OpenAI from "openai";
import type { ClassifiedMessage, EmailMetadata } from "../schema.js";
import { buildClassifierPrompt, parseClassifierJson } from "./classifier.js";

export async function classifyWithOpenAI(
  messages: EmailMetadata[],
): Promise<ClassifiedMessage[]> {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error("OPENAI_API_KEY is required when AI_PROVIDER=openai");
  }

  const client = new OpenAI({ apiKey });
  const model = process.env.OPENAI_MODEL || "gpt-5.4-mini";
  const response = await client.responses.create({
    model,
    input: buildClassifierPrompt(messages),
    text: { format: { type: "json_object" } },
  });

  return parseClassifierJson(
    response.output_text,
    messages.map((message) => message.id),
  );
}
