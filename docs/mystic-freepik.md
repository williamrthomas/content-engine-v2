Of course. Here is a cleaned-up and reorganized guide for developers using the Mystic API, formatted for clarity and ease of use.

-----

## Mystic AI Image Generation API Guide

The Mystic API endpoint allows you to generate ultra-realistic, high-resolution images from text descriptions. It offers a wide range of parameters for fine-tuning the output, including structure and style references, advanced model controls, and detailed styling options.

This is an asynchronous endpoint. You will receive a task ID upon a successful request, and the final image data will be sent to a specified `webhook_url` or can be retrieved later.

-----

### Endpoint

To generate an image, send a **POST** request to the following endpoint:

```
https://api.freepik.com/v1/ai/mystic
```

### Authentication

Authentication is handled via an API key passed in the request headers.

  * **Header**: `x-freepik-api-key`
  * **Value**: `YOUR_API_KEY`

-----

### Request Body Parameters

The following table details all the parameters you can include in your JSON request body.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`prompt`** | string | - | **Required.** The text description of the image you want to generate. Supports special character syntax (see below). |
| `webhook_url` | string | - | An optional callback URL that will receive notifications about the task status. |
| **`structure_reference`** | string | - | A Base64-encoded image to use as a structural reference, influencing the final image's shape and composition. |
| `structure_strength` | integer | 50 | Determines how strongly the output adheres to the `structure_reference` image. Range: `0` to `100`. |
| **`style_reference`** | string | - | A Base64-encoded image to use as a style reference, influencing the aesthetic (colors, textures, mood). |
| `adherence` | integer | 50 | How faithfully the output follows the `prompt` vs. the `style_reference`. Higher values prioritize the prompt. Range: `0` to `100`. |
| `hdr` | integer | 50 | Increases image detail at the cost of a more "AI look." Lower values appear more natural. Range: `0` to `100`. |
| `resolution` | enum | `2k` | The resolution of the generated image. Options: `1k`, `2k`, `4k`. |
| `aspect_ratio` | enum | `square_1_1` | The image's width-to-height ratio. Options include `square_1_1`, `widescreen_16_9`, `social_story_9_16`, etc. |
| `model` | enum | `realism` | The core generation model. **`realism`**: photographic look. **`fluid`**: creative and prompt-adherent. **`zen`**: smoother, cleaner results. |
| `creative_detailing` | integer | 33 | Adds pixel-level detail. High values can introduce artifacts. Range: `0` to `100`. |
| `engine` | enum | `automatic` | The rendering engine. **`Sharpy`** for realistic, sharp photos. **`Illusio`** for smoother illustrations. **`Sparkle`** is a middle ground. |
| `fixed_generation` | boolean | `false` | If `true`, the same request will produce the same image every time, which is useful for fine-tuning. |
| `styling` | object | - | An object containing arrays for advanced `styles`, `characters`, and `colors` to apply to the image. |
| `filter_nsfw` | boolean | `true` | Enables NSFW content filtering. This cannot be disabled by standard API users. |

-----

### Special Prompt Syntax

You can add and control named characters directly within your prompt text.

  * **Including a Character**: Use the `@` symbol followed by the character's name.
      * *Example*: `"A photo of my friend @john smith as an astronaut"`
  * **Modifying Character Strength**: Adjust a character's influence by adding `::strength` (a numerical value).
      * *Example*: `"A photo of my friend @john smith::200 as an astronaut"`

-----

### Success Response (200 OK)

If the request is successful, the API returns a JSON object confirming that the task has started.

**Example Response Payload:**

```json
{
  "status": "CREATED",
  "task_id": "046b6c7f-0b8a-43b9-b35d-6489e6daee91",
  "generated": []
}
```

  * **`status`**: Indicates the current state of the task.
  * **`task_id`**: A unique identifier for your image generation job.
  * **`generated`**: This array will be populated with image URLs upon task completion, which will be sent to your `webhook_url`.

-----

### Example: Python Request

Here’s a complete example of how to make a request using Python. This includes a helper function to encode your local images into Base64 for use as references.

```python
import requests
import base64
import os

# Helper function to encode an image file to a Base64 string
def encode_image_to_base64(image_path):
    """Encodes a local image file to a Base64 string."""
    if not os.path.exists(image_path):
        print(f"Warning: Image path not found: {image_path}")
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# --- Configuration ---
API_KEY = "YOUR_API_KEY"  # Replace with your actual Freepik API key
API_URL = "https://api.freepik.com/v1/ai/mystic"

# Encode local images for structure and style references (optional)
# structure_image_b64 = encode_image_to_base64("path/to/your/structure_image.jpg")
# style_image_b64 = encode_image_to_base64("path/to/your/style_image.png")

# --- API Request Payload ---
payload = {
    "prompt": "A majestic golden dragon flying through a vibrant nebula, cinematic lighting",
    "aspect_ratio": "widescreen_16_9",
    "model": "fluid",
    "resolution": "2k",
    "creative_detailing": 50,
    # "style_reference": style_image_b64, # Uncomment to use a style reference
    # "adherence": 60,                   # Uncomment to adjust style adherence
}

# --- Set Headers ---
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "x-freepik-api-key": API_KEY
}

# --- Send Request ---
try:
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    # --- Print Response ---
    print("Request successful!")
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())

except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")
    print(f"Response Content: {err.response.text}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

```