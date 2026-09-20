import os
from openai import OpenAI


def get_ai_analysis(traffic_data):
    api_key = os.getenv("TRAFFIC_AI_API_KEY")
    base_url = os.getenv("TRAFFIC_AI_BASE_URL")
    model = os.getenv("TRAFFIC_AI_MODEL")

    if not api_key:
        return "AI API key not configured."

    if not base_url:
        return "AI base URL not configured."

    if not model:
        return "AI model not configured."

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        prompt = f"""
You are an AI traffic management assistant.

IMPORTANT:
The vehicle counts below come from computer vision.
Do NOT change, invent, or estimate the vehicle counts.

Traffic data:
Road A: {traffic_data["Road A"]} vehicles
Road B: {traffic_data["Road B"]} vehicles
Road C: {traffic_data["Road C"]} vehicles
Road D: {traffic_data["Road D"]} vehicles

Emergency: {traffic_data["Emergency"]}

Current signal: {traffic_data["Current Signal"]}
Green time: {traffic_data["Green Time"]} seconds

Give a short traffic analysis.

Include:
1. Highest traffic road
2. Traffic summary
3. Why the current signal timing is appropriate
4. Emergency explanation if emergency is active

Keep the answer short and suitable for a dashboard.
"""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a traffic analysis assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=250
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis error: {str(e)}"