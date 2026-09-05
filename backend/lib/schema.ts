import { z } from "zod";

export const ClassificationSchema = z.enum([
  "spam",
  "promotion",
  "action_required",
  "keep",
  "uncertain",
]);

export const RecommendedActionSchema = z.enum(["trash", "keep", "review"]);

export const EmailMetadataSchema = z.object({
  id: z.string().min(1).max(512),
  accountId: z.string().min(1).max(128).optional(),
  from: z
    .object({
      address: z.string().email().optional(),
      name: z.string().max(256).optional(),
    })
    .optional(),
  subject: z.string().max(1000).optional(),
  snippet: z.string().max(4000).optional(),
  date: z.number().int().optional(),
  folders: z.array(z.string().max(128)).max(50).optional(),
});

export const ClassifyRequestSchema = z.object({
  messages: z.array(EmailMetadataSchema).min(1).max(50),
});

export const ClassifiedMessageSchema = z.object({
  id: z.string().min(1),
  classification: ClassificationSchema,
  recommendedAction: RecommendedActionSchema,
  confidence: z.number().min(0).max(1),
  reason: z.string().min(1).max(500),
});

export const ClassifyResponseSchema = z.object({
  provider: z.enum(["gemini", "openai"]),
  messages: z.array(ClassifiedMessageSchema).max(50),
});

export type EmailMetadata = z.infer<typeof EmailMetadataSchema>;
export type ClassifyRequest = z.infer<typeof ClassifyRequestSchema>;
export type ClassifyResponse = z.infer<typeof ClassifyResponseSchema>;
export type ClassifiedMessage = z.infer<typeof ClassifiedMessageSchema>;
