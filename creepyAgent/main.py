from ai_app import agent

user_prompt = "where can i find information on the next function?"

stream = agent.stream_events({"messages": [{"role": "user", "content": user_prompt}]}, version="v3")

for kind, item in stream.interleave("messages", "tool_calls"):
    if kind == "messages":
        for token in item.text:
            print(token, end="", flush=True)
        for bad_call in getattr(item, "invalid_tool_calls", []):
            print(f"\nInvalid tool call for {bad_call['name']}")
    elif kind == "tool_calls":
        print(f"tool call: {item.tool_name}")

