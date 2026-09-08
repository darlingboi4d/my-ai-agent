# tools.py — your agent's tools

# ----------------------------------------------------------------------
# PART 1: Your tool functions (ordinary Python — the data can be fake)
# ----------------------------------------------------------------------

# This is a dictionary. Think of it as a price list on a shop wall.
PRICES = {
    "rice": 85000,
    "beans": 62000,
    "garri": 28000,
    "yam": 45000,
    "plantain": 35000,
}

def get_price(item):
    """
    Return the market price of an item in Naira.
    
    What happens:
    1. We take the item name and make it lowercase + strip spaces
       (so "Rice ", "RICE", and "rice" all match)
    2. We look it up in our PRICES dictionary
    3. If found, we return a nice formatted string
    4. If not found, we return a helpful error message
    """
    key = item.lower().strip()  # Clean up the input
    if key in PRICES:
        return f"{item}: ₦{PRICES[key]:,} per bag"
    return f"No price data for {item}."


def calculate_total(price_per_unit, quantity):
    """
    Multiply a unit price by a quantity.
    
    What happens:
    1. We convert both inputs to numbers (float)
    2. We multiply them
    3. We return a nicely formatted total
    """
    total = float(price_per_unit) * float(quantity)
    return f"Total: ₦{total:,.0f}"


def compare_items(item_a, item_b):
    """
    Compare the prices of two items.
    
    What happens:
    1. Clean both item names
    2. Look up both prices
    3. Figure out which is cheaper and by how much
    4. Return a clear comparison
    """
    a = item_a.lower().strip()
    b = item_b.lower().strip()
    
    if a in PRICES and b in PRICES:
        cheaper = item_a if PRICES[a] < PRICES[b] else item_b
        diff = abs(PRICES[a] - PRICES[b])
        return f"{cheaper} is cheaper by ₦{diff:,}"
    
    return "I don't have prices for both items."


# ----------------------------------------------------------------------
# PART 2: Describe each tool to the model (THE MENU)
# ----------------------------------------------------------------------

"""
This is the MOST IMPORTANT part for beginners to understand.

The LLM cannot "see" your Python functions. It doesn't know they exist.
You must describe each tool in a special format called JSON Schema.

Think of TOOL_SCHEMAS as a restaurant menu:
- Name of the dish (function name)
- Description of what it does (so the customer knows when to order it)
- What ingredients it needs (parameters)

If your descriptions are vague, the LLM will order the wrong dish.
If your parameter names don't match your function names, the kitchen crashes.
"""

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "Get the current market price of a food item in Naira. Use this when the user asks how much something costs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The item name, e.g. rice, beans, garri"
                    }
                },
                "required": ["item"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total",
            "description": "Multiply a unit price by a quantity to get a total cost. Use this when the user wants to know the total for multiple items.",
            "parameters": {
                "type": "object",
                "properties": {
                    "price_per_unit": {
                        "type": "number",
                        "description": "Price of one unit in Naira"
                    },
                    "quantity": {
                        "type": "number",
                        "description": "How many units the user wants to buy"
                    },
                },
                "required": ["price_per_unit", "quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_items",
            "description": "Compare the prices of two food items and say which is cheaper. Use this when the user asks which item costs less.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_a": {
                        "type": "string",
                        "description": "First item to compare"
                    },
                    "item_b": {
                        "type": "string",
                        "description": "Second item to compare"
                    },
                },
                "required": ["item_a", "item_b"],
            },
        },
    },
]


# ----------------------------------------------------------------------
# PART 3: The dispatcher (the switchboard operator)
# ----------------------------------------------------------------------

def call_tool(name, args):
    """
    This function is like a switchboard operator.
    
    The LLM says: "I want to use tool X with arguments Y."
    This function receives that request and routes it to the right tool.
    
    Why we need this:
    The LLM only knows the tool NAMES (from the schema).
    It doesn't know how to actually RUN the Python function.
    This bridge connects the LLM's request to the real code.
    """
    if name == "get_price":
        return get_price(**args)
    elif name == "calculate_total":
        return calculate_total(**args)
    elif name == "compare_items":
        return compare_items(**args)
    return f"Unknown tool: {name}"


# ----------------------------------------------------------------------
# PART 4: Quick test (delete this section before submitting)
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("--- Testing get_price ---")
    print(get_price("rice"))
    print(get_price("gold"))  # Should fail gracefully
    
    print("\n--- Testing calculate_total ---")
    print(calculate_total(85000, 3))
    
    print("\n--- Testing compare_items ---")
    print(compare_items("rice", "beans"))
    
    print("\n--- Testing call_tool dispatcher ---")
    print(call_tool("get_price", {"item": "garri"}))
    print(call_tool("calculate_total", {"price_per_unit": 28000, "quantity": 5}))