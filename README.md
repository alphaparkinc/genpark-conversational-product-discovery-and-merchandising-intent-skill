# genpark-conversational-product-discovery-and-merchandising-intent-skill

Semantic conversational product discovery, facet intent extraction, and merchandising ranking engine for e-commerce agents.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Conversational Intent Extraction**: Deconstructs freeform shopping requests into structured merchandising dimensions (e.g. price limits, target demographics, functional attributes, and core search keywords).
- **Multi-Factor Merchandising Ranker**: Combines semantic query alignment, attribute coverage, demographic affinity, inventory availability, and merchant promotional boost weights.
- **Clarification Facet Generation**: Synthesizes smart follow-up clarification prompts when customer intent is underspecified to streamline guided selling workflows.
- **Zero-Dependency Lightweight Core**: High-throughput catalog filtering with standard library regular expressions and tokenizers.

## Architecture

```
[Conversational User Prompt]
              │
              ▼
┌──────────────────────────────────────────────┐
│        ConversationalDiscoveryEngine         │
│  - Price Constraint RegEx Parser             │
│  - Demographic & Attribute Classifier        │
│  - Token Cleaner & Stopword Remover          │
└──────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────┐
│        Merchandising Ranking Matrix          │
│  Score = (0.45*Token + 0.35*Attr + 0.2*Price)│
│          * DemoScore * MerchBoost * Stock    │
└──────────────────────────────────────────────┘
              │
      ┌───────┴───────┐
      ▼               ▼
[Ranked Products]   [Refinement Questions]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `parse_shopping_intent`: Extracts structured price limits, attributes, and search tokens from customer conversational queries.
- `rank_merchandising_catalog`: Ranks catalog products by matching intent facets and applying business merchandising boosts.
- `generate_refinement_questions`: Generates conversational follow-up questions to refine facets when customer intent is ambiguous.

## Quickstart (Python API)

```python
from client import ConversationalDiscoveryEngine

query = "I need lightweight breathable running shoes for men under $120"
intent = ConversationalDiscoveryEngine.parse_query_intent(query)

catalog = [
    {
        "id": "1",
        "title": "AeroBreeze Men's Lightweight Running Shoes",
        "description": "Breathable mesh runner",
        "tags": ["running", "shoes", "lightweight", "breathable", "men"],
        "price": 109.99,
        "boost_factor": 1.3,
        "in_stock": True,
    }
]

ranked = ConversationalDiscoveryEngine.rank_catalog(catalog, intent)
print("Top match:", ranked[0]["title"], "Score:", ranked[0]["final_score"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
