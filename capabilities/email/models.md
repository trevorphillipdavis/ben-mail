# Email Models

Initial conceptual models for the Email capability.

## EmailAddress

- `name`
- `address`

## EmailMessage

- `id`
- `provider`
- `thread_id`
- `subject`
- `from`
- `to`
- `cc`
- `bcc`
- `sent_at`
- `received_at`
- `body`
- `attachments`

## EmailThread

- `id`
- `provider`
- `subject`
- `participants`
- `messages`

## EmailAttachment

- `id`
- `filename`
- `content_type`
- `size_bytes`
- `provider_reference`
