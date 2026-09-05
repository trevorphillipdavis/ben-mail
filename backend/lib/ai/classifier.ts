import {
  ClassifiedMessageSchema,
  ClassifyResponseSchema,
  type ClassifiedMessage,
  type ClassifyResponse,
  type EmailMetadata,
} from "../schema.js";
import { classifyWithGemini } from "./gemini.js";
import { classifyWithOpenAI } from "./openai.js";

export type AiProvider = "gemini" | "openai";

export function getAiProvider(): AiProvider {
  const provider = (process.env.AI_PROVIDER || "gemini").toLowerCase();
  if (provider === "gemini" || provider === "openai") {
    return provider;
  }
  throw new Error("AI_PROVIDER must be gemini or openai");
}

export async function classifyMessages(messages: EmailMetadata[]): Promise<ClassifyResponse> {
  const provider = getAiProvider();
  const result =
    provider === "openai"
      ? await classifyWithOpenAI(messages)
      : await classifyWithGemini(messages);

  return ClassifyResponseSchema.parse({ provider, messages: result });
}

export function buildClassifierPrompt(messages: EmailMetadata[]): string {
  return [
    "Classify email metadata/snippets for Ben Mail.",
    "The backend never fetches email and never deletes email.",
    "Return strict JSON only. No markdown.",
    "Classifications: spam, promotion, action_required, keep, uncertain.",
    "Recommended actions: trash, keep, review.",
    "Use trash only for clear spam or obvious promotions.",
    "Use keep for finance, tax, legal, insurance, document-signature, account security, orders, shipping, and known human/vendor correspondence.",
    "Use review when uncertain or potentially important.",
    "",
    "Return this shape:",
    '{"messages":[{"id":"...","classification":"spam","recommendedAction":"trash","confidence":0.95,"reason":"short reason"}]}',
    "",
    JSON.stringify({ messages: sanitizeMessages(messages) }),
  ].join("\n");
}

export function parseClassifierJson(raw: string, expectedIds: string[]): ClassifiedMessage[] {
  const cleaned = raw.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/i, "");
  let parsed: unknown;
  try {
    parsed = JSON.parse(cleaned);
  } catch {
    throw new Error("AI provider returned invalid JSON");
  }

  const response = ClassifyResponseSchema.omit({ provider: true }).parse(parsed);
  const expected = new Set(expectedIds);
  const seen = new Set<string>();

  for (const message of response.messages) {
    if (!expected.has(message.id)) {
      throw new Error("AI provider returned an unknown message id");
    }
    if (seen.has(message.id)) {
      throw new Error("AI provider returned a duplicate message id");
    }
    seen.add(message.id);
  }

  if (seen.size !== expected.size) {
    throw new Error("AI provider did not classify every message");
  }

  return response.messages.map((message) => ClassifiedMessageSchema.parse(message));
}

function sanitizeMessages(messages: EmailMetadata[]): EmailMetadata[] {
  return messages.map((message) => ({
    id: message.id,
    accountId: message.accountId,
    from: message.from,
    subject: message.subject,
    snippet: message.snippet,
    date: message.date,
    folders: message.folders,
  }));
}
