import type { VercelRequest, VercelResponse } from "@vercel/node";
import { ZodError } from "zod";
import { classifyMessages } from "../lib/ai/classifier.js";
import { ClassifyRequestSchema } from "../lib/schema.js";

export default async function handler(request: VercelRequest, response: VercelResponse) {
  if (request.method !== "POST") {
    response.setHeader("Allow", "POST");
    response.status(405).json({ error: "Method not allowed" });
    return;
  }

  try {
    const payload = ClassifyRequestSchema.parse(request.body);
    const result = await classifyMessages(payload.messages);
    response.status(200).json(result);
  } catch (error) {
    if (error instanceof ZodError) {
      response.status(400).json({ error: "Invalid request or provider response" });
      return;
    }

    response.status(500).json({ error: "Classification failed" });
  }
}
