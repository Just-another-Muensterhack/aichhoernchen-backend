from agents import set_default_openai_client, Agent, Runner
from openai import AsyncAzureOpenAI
import os
import base64


async def main() -> None:
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource-name.openai.azure.com/")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_llm_model = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")

    azure_client = AsyncAzureOpenAI(
        api_key=azure_api_key,
        azure_endpoint=azure_endpoint
    )

    set_default_openai_client(azure_client)

    agent = Agent(
        name="Image Analysis Agent",
        instructions=open("prompts/image_analysis.md").read(),
        model=azure_llm_model,
    )

    b64_image = base64.b64encode(open("path/to/your/image.jpg", "rb").read()).decode("utf-8")

    result = await Runner.run(
        agent,
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_data": f"data:image/jpeg;base64,{b64_image}",
                        "filename": "image.jpg",
                    }
                ],
            },
            {
                "role": "user",
                "content": "What is the first sentence of the introduction?",
            },
        ],
    )
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
