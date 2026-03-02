# standalone_test.py - Test string extraction from model_output
import re

# Your exact model_output format from the error log
model_output = '''
{
  "action": "read",
  "query": "SELECT * FROM customer INNER JOIN orders ON customer.customer_id = orders.customer_id WHERE orders.order_value > 5;",
  "content": ""
}
'''

print("=== RAW INPUT ===")
print(repr(model_output))
print()

# METHOD 1: String find() - Simple, no regex
start_action = model_output.find('"action": "') + 11
end_action = model_output.find('"', start_action)
action = model_output[start_action:end_action].strip()

start_query = model_output.find('"query": "') + 10
end_query = model_output.find('"', start_query + 1)  # ← Key fix!
query = model_output[start_query:end_query].strip()

print(f"CLEAN: '{query}'")  # Now perfect SQL only




# METHOD 2: Regex - Cleanest (1 line)
print("=== METHOD 2: Regex ===")
match = re.search(r'"action":\s*"([^"]+)".*"query":\s*"([^"]*)"', model_output)
if match:
    action_regex, query_regex = match.groups()
    print(f"Action: '{action_regex}'")
    print(f"Query: '{query_regex}'")
    print(f"Action code: {1 if action_regex == 'read' else 2}")
else:
    print("Regex failed to match!")
print()

# METHOD 3: Test with empty/bad data
print("=== METHOD 3: Edge cases ===")
bad_outputs = [
    "",  # Empty
    None,  # None
    '{"error": "no sql"}',  # Wrong format
]

for bad in bad_outputs:
    print(f"Testing: {repr(bad)}")
    try:
        match = re.search(r'"action":\s*"([^"]+)".*"query":\s*"([^"]*)"', str(bad))
        if match:
            action, query = match.groups()
            print(f"  → Success: {action}, {query[:50]}...")
        else:
            print("  → Failed: No match")
    except:
        print("  → Failed: Exception")
