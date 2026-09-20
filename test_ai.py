import os
from openai import OpenAI


print("=" * 60)
print("TRAFFIC AI API CONNECTION TEST")
print("=" * 60)


api_key = os.getenv("TRAFFIC_AI_API_KEY")
base_url = os.getenv("TRAFFIC_AI_BASE_URL")
model = os.getenv("TRAFFIC_AI_MODEL")


if not api_key:
    print("❌ API key NOT FOUND")
    exit()

print("✅ API key FOUND")
print("🔒 API key is not displayed for security.")


if not base_url:
    print("❌ Base URL NOT FOUND")
    exit()

print("✅ Base URL FOUND")


if not model:
    print("❌ Model NOT FOUND")
    exit()

print(f"✅ Model: {model}")


try:

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    print("✅ AI client created")
    print()
    print("Connecting to AI...")


    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Say: AI traffic system connection successful."
            }
        ],
        temperature=0.2,
        max_tokens=50
    )


    print()
    print("✅ API CONNECTION SUCCESSFUL")
    print()
    print("AI RESPONSE:")
    print(response.choices[0].message.content)


except Exception as e:

    print()
    print("❌ API REQUEST FAILED")
    print()
    print(str(e))