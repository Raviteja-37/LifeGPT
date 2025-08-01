import google.generativeai as genai
import requests
import uuid # To generate a unique ID for each request

import google.generativeai as genai
import requests
# import uuid # No longer needed

def fetch_youtube_results(youtube_pipedream_url, query):
    # Remove the 'Accept' header as well, it's not needed for a standard Pipedream HTTP trigger
    headers = {
        "Content-Type": "application/json"
    }

    # Revert to a simple JSON body with just the 'query'
    request_body = {
        "query": query
    }

    try:
        print(f"DEBUG (Python): Sending simple JSON request body to workflow: {request_body}")
        # Send the simple JSON body
        response = requests.post(youtube_pipedream_url, json=request_body, headers=headers)
        response.raise_for_status()
        data = response.json()

        # The response structure from your Pipedream workflow should be a list of video dictionaries
        # No need for complex JSON-RPC result/error parsing here
        if isinstance(data, list):
            return data
        else:
            # If the Pipedream workflow for some reason returns a dictionary, handle it
            # (though it should be a list based on your workflow's output)
            if isinstance(data, dict):
                return list(data.values())
            else:
                return [{"title": "❌ Unexpected Pipedream Workflow Response Format", "url": f"Got: {data}"}]

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_message += f" - Response content: {e.response.text}"
        return [{"title": "❌ HTTP Error from Pipedream Workflow", "url": error_message}]
    except Exception as e:
        return [{"title": "❌ Unexpected Python Error", "url": str(e)}]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }

    # Construct the JSON-RPC 2.0 compliant request body
    jsonrpc_request_body = {
        "jsonrpc": "2.0",
        "method": "search.list", # <-- CHANGE THIS LINE
        "params": {
            # YouTube Data API's search.list method requires these parameters
            "part": "snippet",
            "type": "video",
            "q": query, # The search query
            "maxResults": 3
        },
        "id": str(uuid.uuid4()) # A unique ID for the request
    }

    try:
        print(f"DEBUG (Python): Sending JSON-RPC request body: {jsonrpc_request_body}")
        response = requests.post(youtube_pipedream_url, json=jsonrpc_request_body, headers=headers)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # The response structure for JSON-RPC is usually {"jsonrpc": "2.0", "result": ..., "id": ...} or {"jsonrpc": "2.0", "error": ..., "id": ...}
        if "result" in data and isinstance(data["result"], dict) and "items" in data["result"]:
            # Extract items from the 'result' and then map them
            videos = []
            for item in data["result"]["items"]:
                if item["id"]["kind"] == "youtube#video": # Ensure it's a video
                    videos.append({
                        "title": item["snippet"]["title"],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                    })
            return videos
        elif "error" in data:
            error_details = data["error"]
            error_message = f"Pipedream MCP Error: {error_details.get('message', 'Unknown error')} (Code: {error_details.get('code', 'N/A')})"
            return [{"title": "❌ MCP Server Error", "url": error_message}]
        else:
            return [{"title": "❌ Unexpected MCP Response", "url": f"Unknown response format: {data}"}]

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_message += f" - Response content: {e.response.text}"
        return [{"title": "❌ Network/HTTP Error with MCP", "url": error_message}]
    except Exception as e:
        return [{"title": "❌ Unexpected Python Error", "url": str(e)}]

def run_agent_sync(
    google_api_key,
    youtube_pipedream_url,
    user_goal,
    progress_callback
):
    try:
        # Configure Gemini SDK
        genai.configure(api_key=google_api_key)

        progress_callback("🔗 Fetching YouTube resources...")
        youtube_videos = fetch_youtube_results(youtube_pipedream_url, user_goal)
        print("📦 YouTube Videos Fetched:", youtube_videos)
        youtube_links_text = "\n".join([f"- {video.get('title')} → {video.get('url')}" for video in youtube_videos])
        print("🧠 YouTube links in prompt:\n", youtube_links_text)


        # System prompt
        system_prompt = f"""
You are LifeGPT, a personal AI learning assistant.

The user wants to achieve this goal: **{user_goal}**

Here are top YouTube videos you MUST consider and recommend across the 5-day plan:

{youtube_links_text or '❌ No videos available'}

Instructions:
- Break down the goal into a 5-day plan.
- Recommend 1–2 YouTube videos per day **from the list above**.
- Use a clear, motivational tone.
- Do NOT mention 'No videos found' unless the list is truly empty.

Output only the structured learning plan.
"""


        progress_callback("⚡ Generating plan using Gemini...")
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(system_prompt)

        progress_callback("✅ Done!")
        return {"messages": [response.text]}

    except Exception as e:
        raise RuntimeError(f"[utils.py] ❌ Error: {str(e)}")
