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

## script for testing
```js
const obj = { 
    text_for_processing: "IDC Government Insights: Worldwide Railways and Airlines IT Strategies empowers executives in railway operators, railway infrastructure companies and airlines to make evidence-based decisions about the future of customer experience, revenue management and net-zero, safe, and resilient operations. The service will enable executives to understand how technology will impact ticketing, booking, revenue management, linear asset and fleet maintenance and operations and trigger innovative collaborations across the passenger transportation ecosystem. Markets and Subjects Analyzed Connected customer experience Revenue innovation and management Safe, sustainable, and resilient operations Core Next-generation ticketing and revenue management in railways and airlines IDC MarketScape: European Digital Twin Professional Services for the Transportation Ecosystem Vendor Assessment The power of digital and data in the air travel ecosystem FRMCS: the power of 5G for the railway industry In addition to the insight provided in this service, IDC may conduct research on specific topics or emerging market segments via research offerings that require additional IDC funding and client investment. Key Questions Answered How will technology innovation trigger change in the future of railway and airline customer experience? How will technology innovation enable railways and airlines to save fuel/energy, and increase employee productivity, while maintaining high safety standards? How can technology suppliers reimagine their portfolio and go-to-market to be best positioned to deliver successful solutions in the future of railways and airlines? How will railways and airlines work with the passenger transportation ecosystem to enable end-to-end mobility as a service experience? What are the organizational change, security, technical, legal, and project management challenges that need to be addressed to unleash the benefits of technology innovation for railways and airlines?",
    tags: [
        "realistic",
        "8k",
        "octane render",
        "cinematic",
        "trending on artstation",
        "cinematic composition"
    ]
};

const request = new Request("/backend/textToPrompt", {
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