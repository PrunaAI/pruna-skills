# Pruna Client

Official Pruna API client for image and video generation and editing.

## Installation

```bash
uv add pruna-client
```

## Quick Start

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

# Initialize client (uses PRUNA_API_KEY env var if api_key not provided)
client = PrunaClient()  # or PrunaClient(api_key="your_api_key")

# Generate image
response = client.generate_text_to_image(
    model="p-image",
    prompt="A beautiful sunset over a calm ocean",
    sync=True,
)

# Access the generated content via generation_url
if response.status == PredictionStatus.SUCCEEDED:
    generation_url = response.response.get("generation_url")
    if generation_url:
        # Download the generated image
        image_bytes = client.download_content(generation_url)
        with open("generated_image.jpg", "wb") as f:
            f.write(image_bytes)
```

## Accessing Generated Content

**Important:** All successful generation responses contain a `generation_url` in `response.response["generation_url"]` that points to the generated content (image or video). You can download this content using the `download_content()` method.

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

client = PrunaClient()

# After generating content
response = client.generate_text_to_image(
    model="p-image",
    prompt="A beautiful sunset",
    sync=True
)

if response.status == PredictionStatus.SUCCEEDED:
    generation_url = response.response.get("generation_url")
    if generation_url:
        # Download the generated content
        content = client.download_content(generation_url)
        with open("output.jpg", "wb") as f:  # or .mp4 for videos
            f.write(content)
```

## Basic Usage

### General Generation

We support both batch and single generation for any model. You only need to call the `generate` or `generate_batch` method with the required parameters as shown on [Pruna API Reference](https://ac25aba50212.eu.kongportals.com/)

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

client = PrunaClient()

# Single generation
response = client.generate(
    model="p-image",
    input={"prompt": "A beautiful sunset over a calm ocean"},
    sync=True
)

# Access the generated content via generation_url
if response.status == PredictionStatus.SUCCEEDED:
    generation_url = response.response.get("generation_url")
    if generation_url:
        content = client.download_content(generation_url)
        with open("output.jpg", "wb") as f:
            f.write(content)

# Batch generation
responses = client.generate_batch(
    requests=[
        {"model": "p-image", "input": {"prompt": "A sunset"}, "sync": True},
        {"model": "p-image", "input": {"prompt": "A sunrise"}, "sync": True},
    ]
)

# Access generation URLs from batch responses
for i, response in enumerate(responses):
    if response.status == PredictionStatus.SUCCEEDED:
        generation_url = response.response.get("generation_url")
        if generation_url:
            content = client.download_content(generation_url)
            with open(f"output_{i}.jpg", "wb") as f:
                f.write(content)
```

### Specific Models

We support specific models for image and video generation and editing. You only need to call the `generate_text_to_image`, `generate_image_edit`, `generate_text_to_video`, `generate_video_edit`, `generate_image_to_video` method with the required parameters as shown on [Pruna API Reference](https://ac25aba50212.eu.kongportals.com/)

### Text to Image

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

client = PrunaClient()

# Generate with default parameters
response = client.generate_text_to_image(
    model="p-image",
    prompt="A beautiful sunset over a calm ocean",
    sync=True
)

# The response contains a generation_url with the generated content
if response.status == PredictionStatus.SUCCEEDED:
    generation_url = response.response.get("generation_url")
    if generation_url:
        # Download the generated image
        image_bytes = client.download_content(generation_url)
        with open("generated_image.jpg", "wb") as f:
            f.write(image_bytes)

# Generate with custom parameters
response = client.generate_text_to_image(
    model="p-image",
    prompt="A serene mountain landscape at dawn",
    sync=True,
    aspect_ratio="custom",
    width=512,
    height=512,
)
```

### Image Editing

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus
from PIL import Image
from pathlib import Path

client = PrunaClient()

# Using file path
response = client.generate_image_edit(
    model="p-image-edit",
    prompt="Make the image blue and add a sunset sky",
    images=["path/to/image.png"],
    sync=True
)

# Access the generated content via generation_url
if response.status == PredictionStatus.SUCCEEDED:
    generation_url = response.response.get("generation_url")
    if generation_url:
        image_bytes = client.download_content(generation_url)
        with open("edited_image.jpg", "wb") as f:
            f.write(image_bytes)

# Using PIL Image
img = Image.open("input.jpg")
response = client.generate_image_edit(
    model="p-image-edit",
    prompt="Transform the image into a watercolor painting style",
    images=[img],
    sync=True
)

# Using Path object
response = client.generate_image_edit(
    model="p-image-edit",
    prompt="Add a beautiful landscape background",
    images=[Path("image.png")],
    sync=True
)

# Using multiple images
response = client.generate_image_edit(
    model="p-image-edit",
    prompt="Blend and merge these images into a cohesive composition",
    images=["image1.jpg", "image2.png"],
    sync=True
)

client.close()
```

### Text to Video

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

client = PrunaClient()

# Asynchronous mode (recommended for video generation)
response = client.generate_text_to_video(
    model="wan-t2v",
    prompt="A sports car is driving very fast along a beach at sunset, aerial drone shot, cinematic",
    sync=False
)

# Poll for completion and access generation_url
final_response = client.poll_status(response=response)
if final_response.status == PredictionStatus.SUCCEEDED:
    generation_url = final_response.response.get("generation_url")
    if generation_url:
        video_bytes = client.download_content(generation_url)
        with open("generated_video.mp4", "wb") as f:
            f.write(video_bytes)

```

### Image to Video

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus
from PIL import Image

client = PrunaClient()

# Using file path
response = client.generate_image_to_video(
    model="wan-i2v",
    prompt="The camera slowly pushes in, gentle movement",
    image="path/to/image.jpg",
    sync=False
)

# Using PIL Image
img = Image.open("input.jpg")
response = client.generate_image_to_video(
    model="wan-i2v",
    prompt="Leaves swaying in the wind",
    image=img,
    sync=False
)

# Poll for completion
final_response = client.poll_status(response=response)
if final_response.status == PredictionStatus.SUCCEEDED:
    generation_url = final_response.response.get("generation_url")
    if generation_url:
        video_bytes = client.download_content(generation_url)
        with open("output.mp4", "wb") as f:
            f.write(video_bytes)

client.close()
```

### Video Editing

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

client = PrunaClient()

# Generate video from text only
response = client.generate_video_edit(
    model="vace",
    prompt="A person walking through a magical forest with glowing trees",
    sync=False
)

# Edit existing video
response = client.generate_video_edit(
    model="vace",
    prompt="Add a sunset in the background",
    src_video="input.mp4",
    sync=False
)

# Character-consistent animation with reference images
response = client.generate_video_edit(
    model="vace",
    prompt="Character walking and talking",
    src_ref_images=["character1.jpg", "character2.jpg"],
    sync=False
)

# Poll for completion
final_response = client.poll_status(response=response)
if final_response.status == PredictionStatus.SUCCEEDED:
    generation_url = final_response.response.get("generation_url")
    if generation_url:
        video_bytes = client.download_content(generation_url)
        with open("output.mp4", "wb") as f:
            f.write(video_bytes)
```

## Async Usage

The client supports async operations for better performance when making multiple requests or integrating with async applications.

### General Generation (Async)

```python
import asyncio
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

async def main():
    client = PrunaClient()
    
    response = await client.agenerate(
        model="p-image",
        input={"prompt": "A beautiful sunset over a calm ocean"},
        sync=True
    )
    
    # Access the generated content via generation_url
    if response.status == PredictionStatus.SUCCEEDED:
        generation_url = response.response.get("generation_url")
        if generation_url:
            content = client.download_content(generation_url)
            with open("output.jpg", "wb") as f:
                f.write(content)
    
    await client.aclose()

asyncio.run(main())

# Batch async generation
async def batch_example():
    client = PrunaClient()
    responses = await client.agenerate_batch(
        requests=[
            {"model": "p-image", "input": {"prompt": "A beautiful sunset over a calm ocean"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "A beautiful sunrise over a calm ocean"}, "sync": True},
        ]
    )
    
    # Access generation URLs from batch responses
    for i, response in enumerate(responses):
        if response.status == PredictionStatus.SUCCEEDED:
            generation_url = response.response.get("generation_url")
            if generation_url:
                content = client.download_content(generation_url)
                with open(f"output_{i}.jpg", "wb") as f:
                    f.write(content)
    
    await client.aclose()

asyncio.run(batch_example())
```

## Additional methods

We support additional methods for file upload, polling status, and closing the client. You only need to call the `upload_file`, `poll_status`, `close` method with the required parameters as shown on [Pruna API Reference](https://ac25aba50212.eu.kongportals.com/)

### File Upload

We support `string`, `pathlib.Path`, `PIL.Image.Image`, and `bytes` as input.

```python
from pruna_client import PrunaClient
from pathlib import Path
from PIL import Image

client = PrunaClient()

# Upload from file path
url = client.upload_file("path/to/image.png")

# Upload PIL Image
img = Image.open("input.jpg")
url = client.upload_file(img)

# Upload from Path object
path = Path("image.png")
url = client.upload_file(path)

# Upload bytes
with open("image.jpg", "rb") as f:
    image_bytes = f.read()
url = client.upload_file(image_bytes)

# Batch upload
urls = client.upload_file_batch(["path/to/image.png", "path/to/image2.png"])
```

### Polling Status

This method is used to poll the status of a generation request and return the final response.

```python
from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

client = PrunaClient()

# Start async generation
response = client.generate(
    model="p-image",
    input={"prompt": "A sunset"},
    sync=False
)

# Poll for completion using response object
final_response = client.poll_status(response=response)

# Or poll using status URL directly
status_url = response.response.get("get_url")
final_response = client.poll_status(status_url=status_url)

if final_response.status == PredictionStatus.SUCCEEDED:
    generation_url = final_response.response.get("generation_url")
    if generation_url:
        content = client.download_content(generation_url)
        with open("output.jpg", "wb") as f:
            f.write(content)

```

## Configuration

The client supports several environment variables to configure its behavior:

### Polling Configuration

- **`DEFAULT_PRUNA_POLL_INTERVAL`** (default: `0.5`): The default interval in seconds between status polling requests when waiting for async generation to complete. This value is used if the API response doesn't include an `X-Poll-Interval` header.

- **`DEFAULT_PRUNA_MAX_WAIT`** (default: `600`): The maximum time in seconds to wait for a generation request to complete before timing out. This value is used if the API response doesn't include an `X-Max-Wait` header.

### Cache Configuration

- **`CACHE_MAXSIZE`** (default: `10000`): The maximum number of file upload entries to cache. The client uses a TTL cache to avoid re-uploading the same files.

- **`CACHE_TTL`** (default: `600`): The time-to-live in seconds for cached file upload entries. After this time, cached entries expire and files will be re-uploaded if requested again.

Example:

```bash
export DEFAULT_PRUNA_POLL_INTERVAL=1.0
export DEFAULT_PRUNA_MAX_WAIT=1200
export CACHE_MAXSIZE=5000
export CACHE_TTL=300
```

## Running Tests

```bash
uv run pytest tests/integration/test_general.py -v
uv run pytest tests/integration/test_text_to_image.py -v
uv run pytest tests/integration/test_image_edit.py -v
uv run pytest tests/integration/test_text_to_video.py -v
uv run pytest tests/integration/test_video_edit.py -v
uv run pytest tests/integration/test_image_to_video.py -v
uv run pytest tests/integration/test_batch_generation.py -v
```

Tests require `PRUNA_API_KEY` environment variable to be set.
