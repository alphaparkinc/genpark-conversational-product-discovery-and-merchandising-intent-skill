"""Conversational Product Discovery and Merchandising Intent Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional
import re


class ConversationalDiscoveryEngine:
    """Parses free-form customer shopping queries into structured merchandising facets,
    and ranks product catalog candidates using facet alignment and business boost heuristics."""

    PRICE_PATTERN = re.compile(r'(?:under|below|less than|<|\$)\s*(\d+(?:\.\d{1,2})?)', re.IGNORECASE)
    GENDER_KEYWORDS = {
        "men": ["men", "mens", "man", "male"],
        "women": ["women", "womens", "woman", "female", "ladies"],
        "kids": ["kids", "children", "boys", "girls", "toddler"],
    }

    @classmethod
    def parse_query_intent(cls, query: str) -> Dict[str, Any]:
        """Extracts structured search intents, budget boundaries, and descriptive attributes from conversational input."""
        q_lower = query.lower()
        extracted_facets: Dict[str, Any] = {
            "raw_query": query,
            "max_price": None,
            "gender_target": None,
            "attributes": [],
            "search_tokens": [],
        }

        # Extract price limit
        price_match = cls.PRICE_PATTERN.search(q_lower)
        if price_match:
            try:
                extracted_facets["max_price"] = float(price_match.group(1))
            except ValueError:
                pass

        # Extract target demographic
        for gender, kw_list in cls.GENDER_KEYWORDS.items():
            if any(re.search(rf'\b{kw}\b', q_lower) for kw in kw_list):
                extracted_facets["gender_target"] = gender
                break

        # Tokenize cleaning noise words
        stop_words = {
            "i", "need", "want", "looking", "for", "a", "an", "the", "in", "with",
            "some", "and", "or", "to", "buy", "under", "below", "less", "than", "of"
        }
        tokens = re.findall(r'[a-zA-Z0-9]+', q_lower)
        filtered_tokens = [t for t in tokens if t not in stop_words and not t.isdigit()]
        extracted_facets["search_tokens"] = filtered_tokens

        # Identify attribute descriptors
        common_attributes = [
            "lightweight", "breathable", "waterproof", "durable", "compact",
            "wireless", "ergonomic", "organic", "cotton", "leather", "running",
            "outdoor", "casual", "smart", "portable", "rechargeable", "insulated"
        ]
        for attr in common_attributes:
            if attr in q_lower:
                extracted_facets["attributes"].append(attr)

        return extracted_facets

    @classmethod
    def rank_catalog(
        cls,
        catalog: List[Dict[str, Any]],
        parsed_intent: Dict[str, Any],
        merchandising_boost_weight: float = 0.25,
    ) -> List[Dict[str, Any]]:
        """Scores and ranks a catalog of products against extracted intent and business merchandising rules."""
        search_tokens = set(parsed_intent.get("search_tokens", []))
        attributes = set(parsed_intent.get("attributes", []))
        max_price = parsed_intent.get("max_price")
        gender_target = parsed_intent.get("gender_target")

        ranked_results = []

        for item in catalog:
            item_id = item.get("id", "")
            title = str(item.get("title", "")).lower()
            description = str(item.get("description", "")).lower()
            tags = [str(t).lower() for t in item.get("tags", [])]
            price = float(item.get("price", 0.0))
            boost = float(item.get("boost_factor", 1.0))
            in_stock = bool(item.get("in_stock", True))

            # Hard filter: out of stock penalty
            if not in_stock:
                stock_mult = 0.2
            else:
                stock_mult = 1.0

            # Price compliance
            price_score = 1.0
            if max_price is not None:
                if price <= max_price:
                    price_score = 1.0 + (max_price - price) / max_price * 0.2
                else:
                    # Penalize over budget items heavily
                    price_score = max(0.05, 1.0 - (price - max_price) / max_price)

            # Text relevance score
            item_text = f"{title} {description} {' '.join(tags)}"
            token_matches = sum(1 for t in search_tokens if t in item_text)
            token_score = (token_matches / len(search_tokens)) if search_tokens else 0.5

            # Attribute match score
            attr_matches = sum(1 for a in attributes if a in item_text)
            attr_score = (attr_matches / len(attributes)) if attributes else 0.5

            # Demographic alignment
            demo_score = 1.0
            if gender_target:
                if gender_target in item_text:
                    demo_score = 1.3
                elif any(other in item_text for other in cls.GENDER_KEYWORDS if other != gender_target):
                    demo_score = 0.5

            # Merchandising business boost
            merch_score = 1.0 + (boost - 1.0) * merchandising_boost_weight

            final_score = (
                (0.45 * token_score + 0.35 * attr_score + 0.20 * price_score)
                * demo_score
                * merch_score
                * stock_mult
            )

            ranked_results.append({
                "id": item_id,
                "title": item.get("title"),
                "price": price,
                "final_score": round(final_score, 4),
                "in_stock": in_stock,
                "matched_tokens": [t for t in search_tokens if t in item_text],
                "matched_attributes": [a for a in attributes if a in item_text],
                "price_compliant": (price <= max_price) if max_price is not None else True,
            })

        # Sort descending by score
        ranked_results.sort(key=lambda x: x["final_score"], reverse=True)
        return ranked_results

    @classmethod
    def generate_follow_up_facets(
        cls,
        parsed_intent: Dict[str, Any],
        ranked_results: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Suggests clarifying follow-up refinement questions for conversational commerce agents."""
        suggestions = []
        if not parsed_intent.get("max_price"):
            suggestions.append({
                "facet_type": "budget_clarification",
                "question": "What is your target budget or maximum price range?",
            })
        if not parsed_intent.get("gender_target"):
            suggestions.append({
                "facet_type": "demographic_filter",
                "question": "Are you shopping for men, women, or unisex styles?",
            })
        if len(parsed_intent.get("attributes", [])) < 2:
            suggestions.append({
                "facet_type": "feature_preference",
                "question": "Do you prefer specific features like waterproof protection, lightweight materials, or breathable fabric?",
            })
        return suggestions
