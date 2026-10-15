"""Example usage for Conversational Product Discovery & Merchandising Intent."""
from client import ConversationalDiscoveryEngine

if __name__ == "__main__":
    # 1. Sample customer conversational query
    query = "I'm looking for lightweight breathable running shoes for men under $130"
    intent = ConversationalDiscoveryEngine.parse_query_intent(query)
    print("Parsed Intent:")
    print("  Max Price:", intent["max_price"])
    print("  Gender Target:", intent["gender_target"])
    print("  Extracted Attributes:", intent["attributes"])
    print("  Search Tokens:", intent["search_tokens"])

    # 2. Sample catalog
    catalog = [
        {
            "id": "prod_1",
            "title": "AeroBreeze Men's Lightweight Running Shoes",
            "description": "Ultra breathable mesh design with responsive cushioning.",
            "tags": ["running", "shoes", "lightweight", "breathable", "men"],
            "price": 119.99,
            "boost_factor": 1.4,
            "in_stock": True,
        },
        {
            "id": "prod_2",
            "title": "TrailStorm Waterproof Hiking Boots",
            "description": "Heavy-duty outdoor boots with all-weather traction.",
            "tags": ["boots", "waterproof", "hiking", "outdoor"],
            "price": 149.99,
            "boost_factor": 1.0,
            "in_stock": True,
        },
        {
            "id": "prod_3",
            "title": "CloudWalk Women's Breathable Sneakers",
            "description": "Daily walking sneakers with breathable knit upper.",
            "tags": ["sneakers", "breathable", "women"],
            "price": 89.99,
            "boost_factor": 1.1,
            "in_stock": True,
        },
    ]

    # 3. Rank catalog against intent
    ranked = ConversationalDiscoveryEngine.rank_catalog(catalog, intent)
    print("\nRanked Product Recommendations:")
    for item in ranked:
        print(f"  [{item['final_score']}] {item['title']} - ${item['price']} (Compliant: {item['price_compliant']})")

    # 4. Refinement questions
    questions = ConversationalDiscoveryEngine.generate_follow_up_facets(intent, ranked)
    print("\nSuggested Follow-up Refinements:")
    for q in questions:
        print(f"  - [{q['facet_type']}] {q['question']}")
