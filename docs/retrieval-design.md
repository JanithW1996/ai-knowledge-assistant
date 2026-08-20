# Retrieval Design

## Current approach

The application uses transparent keyword matching:

1. identify the user's role
2. filter documents by permitted roles
3. split authorised documents into paragraph chunks
4. compare question terms with passage terms
5. rank passages by matching-term count
6. build size-limited context with citations

## Security order

```text
Authorise document
        ↓
Read document
        ↓
Create passages
        ↓
Calculate relevance
        ↓
Build controlled context