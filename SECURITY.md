# Security Policy

This project is experimental. Do not place credentials, private datasets, sensitive personal data, or operational secrets in graph documents or issues.

## Reporting

Do not publish exploitable vulnerability details in public issues. Use GitHub private vulnerability reporting or a private security advisory only if enabled for this repository. No dedicated private reporting address is published here; if GitHub private reporting is unavailable, the owner must configure an approved private reporting channel before production use. Do not include secrets or sensitive personal data in public channels.

## Security boundary

The library validates graph structure, bounded fields and referential integrity. It does not provide access control, encryption, authorization, tamper-proof storage, source authenticity, or truth verification. Deployers must enforce those controls outside this library.
