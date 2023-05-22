# article-image-generator
## Table of contents

- [Table of contents](#table-of-contents)
    - [About:](#about)
    - [Technologies:](#technologies)
    - [AI Models:](#ai-models)
    - [Requirements:](#requirements)
- [Getting Started:](#getting-started)

## About:
Article image generator is a web application that generates headline images for articles. It's build on GPT-3.5, Stable diffusion 2.1 and our custom model for image validation. The application is built with Svelte and FastAPI.

### Technologies:
1. Frontend: [Svelte](https://svelte.dev/) - Svelte is a modern JavaScript framework that enables the development of interactive user interfaces
2. Backend: [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a powerful Python framework for building web applications.

### AI Models:
1. Image generation: [Stable diffusion 2.1](https://stability.ai/blog/stable-diffusion-public-release) - Stable diffusion 2.1 is an advanced AI model specifically designed for generating high-quality images
2. Text processing: [gpt-35-turbo](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) - cutting-edge text processing model developed by OpenAI

### Requirements: 
1. [Python 3.9.2](https://www.python.org/downloads/) - Python serves as the primary programming language for the backend implementation.
2. [NodeJS 18.16.0 LTS](https://nodejs.org/en) - NodeJS is essential for running the Svelte frontend and managing the necessary dependencies.

## Getting Started:

1. Create Python virtual enviroment (optional, but will prevent some unexpected errors)
    - when you restart your workspace you will need to activate it again, just run the second line

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Get all svelte packages

```cmd
cd ./frontend
npm install
cd ../
```

3. Build svelte and run fastapi

```cmd
cd ./frontend
npm run build
cd ../
python main.py
```

4. When first build is done, just run the python file
    - don't forget to be in virtual enviroment

```cmd
python main.py
```

## scripts for testing
### javascript
```js
const obj = { 
    text_for_processing: "Yellow submarine with a red hat",
    image_look: "realistic"
};

const request = new Request("/backend/text-to-image", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(obj),
});

fetch(request).then((data) => {
  console.log(data.json());
});
```

### Curl:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "text_for_processing": "Yellow submarine with a red hat",
  "image_look": "realistic"
}' http://127.0.0.1:8001/backend/text-to-image
```

### Powershell:
```powershell
$uri = "http://127.0.0.1:8001/backend/text-to-image"

$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    "text_for_processing" = "Yellow submarine with a red hat"
    "image_look" = "realistic"
}

$response = Invoke-RestMethod -Uri $uri -Method POST -Headers $headers -Body ($body | ConvertTo-Json)

$response
```