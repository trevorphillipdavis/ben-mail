# Email Interface

This document defines the initial Email capability interface at a conceptual level.

## Operations

### Send Email

Inputs:

- Recipient list
- Subject
- Body
- Optional CC and BCC
- Optional attachments

Output:

- Provider message identifier
- Delivery or submission status

### Search Email

Inputs:

- Query
- Optional date range
- Optional sender or recipient filters
- Optional pagination settings

Output:

- Message summaries
- Provider cursors or continuation tokens when available

### Read Thread

Inputs:

- Thread identifier

Output:

- Thread metadata
- Ordered messages
- Attachments metadata

### Reply To Email

Inputs:

- Message or thread identifier
- Reply body
- Optional recipients
- Optional attachments

Output:

- Provider message identifier
- Delivery or submission status

## Notes

This interface is intentionally provider-neutral. Provider-specific identifiers may be carried as opaque values but should not leak into orchestrator behavior.
