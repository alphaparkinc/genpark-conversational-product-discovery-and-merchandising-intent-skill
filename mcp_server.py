"""MCP server for Conversational Product Discovery & Merchandising Intent."""
import sys
import json
from client import ConversationalDiscoveryEngine


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "parse_shopping_intent",
                    "description": "Extracts structured price limits, attributes, and search tokens from customer conversational queries",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Freeform shopping query from user"}
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "rank_merchandising_catalog",
                    "description": "Ranks catalog products by matching intent facets and applying business merchandising boosts",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "catalog": {"type": "array", "description": "Array of product catalog records"},
                            "parsed_intent": {"type": "object", "description": "Structured intent extracted from user query"},
                            "merchandising_boost_weight": {"type": "number", "default": 0.25},
                        },
                        "required": ["catalog", "parsed_intent"],
                    },
                },
                {
                    "name": "generate_refinement_questions",
                    "description": "Generates conversational follow-up questions to refine facets when customer intent is ambiguous",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "parsed_intent": {"type": "object"},
                            "ranked_results": {"type": "array"},
                        },
                        "required": ["parsed_intent"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "parse_shopping_intent":
            res = ConversationalDiscoveryEngine.parse_query_intent(args.get("query", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "rank_merchandising_catalog":
            res = ConversationalDiscoveryEngine.rank_catalog(
                args.get("catalog", []),
                args.get("parsed_intent", {}),
                merchandising_boost_weight=args.get("merchandising_boost_weight", 0.25),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "generate_refinement_questions":
            res = ConversationalDiscoveryEngine.generate_follow_up_facets(
                args.get("parsed_intent", {}),
                args.get("ranked_results", []),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
