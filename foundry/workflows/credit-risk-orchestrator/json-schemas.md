# JSON Schemas

Use these schemas in the Foundry workflow designer when configuring structured agent outputs.

## Router Output

```json
{
  "name": "credit_risk_route",
  "schema": {
    "type": "object",
    "properties": {
      "route": {
        "type": "string",
        "enum": ["policy", "loan_file", "governance", "human_review", "unsupported"]
      },
      "reason": {
        "type": "string"
      },
      "confidence": {
        "type": "number"
      }
    },
    "required": ["route", "reason", "confidence"],
    "additionalProperties": false
  },
  "strict": true
}
```

## Specialist Output

```json
{
  "name": "credit_risk_specialist_result",
  "schema": {
    "type": "object",
    "properties": {
      "summary": {
        "type": "string"
      },
      "required_action": {
        "type": "string"
      },
      "human_review_required": {
        "type": "boolean"
      },
      "sources": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },
    "required": ["summary", "required_action", "human_review_required", "sources"],
    "additionalProperties": false
  },
  "strict": true
}
```

## Governance Output

```json
{
  "name": "credit_risk_governance_result",
  "schema": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "enum": ["allowed", "restricted", "blocked", "needs_review"]
      },
      "risk_level": {
        "type": "string",
        "enum": ["low", "medium", "high"]
      },
      "required_controls": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "explanation": {
        "type": "string"
      }
    },
    "required": ["status", "risk_level", "required_controls", "explanation"],
    "additionalProperties": false
  },
  "strict": true
}
```

