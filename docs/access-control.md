# Access Control

## Classifications

| Classification | Meaning |
|---|---|
| Public | Safe for anyone to view |
| Internal | Available to all authenticated employees |
| Restricted | Available only to specifically authorised roles |

## Role permissions

| Role | Public | Internal | Restricted HR | Restricted Manager | Restricted IT |
|---|---:|---:|---:|---:|---:|
| Employee | Yes | Yes | No | No | No |
| Manager | Yes | Yes | No | Yes | No |
| HR Adviser | Yes | Yes | Yes | No | No |
| IT Support Officer | Yes | Yes | No | No | Yes |

## Enforcement rule

The application must check the user’s role and the document’s classification before retrieving document content.

The AI model must never decide whether access is allowed.