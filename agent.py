from idlelib.history import History

from langchain_openai import AzureChatOpenAI
from browser_use import Agent,Browser
from openai.types.responses.response_file_search_tool_call import Result
from pydantic import SecretStr
from dotenv import load_dotenv
import os
from browser_use import BrowserConfig
import asyncio
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

browser=Browser(
    config = BrowserConfig(
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        
        disable_security=True,
    )

)


# Initialize the model
llm = AzureChatOpenAI(
    model="gpt-4o",
    api_version='2025-01-01-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
    api_key=SecretStr(os.getenv('AZURE_OPENAI_KEY', '')),
    azure_deployment="gpt-4o-2"
)

# llm = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0.0,
# )

# Create agent with the model
agent = Agent(
    task="Go to  https://www.marktplaats.nl/l/auto-s/q/audi/. This site is in Dutch language"
         " click on each listing and go to the detail page . Then clicking on the button with the text (Toon nummer)"
         "This will open a popup with the phone number. Extract that phone number. If you don't find the phone number then leave it blank."
         "Close the popup and go back to the listing and continue till all the listings are done.",
    llm=llm,
    browser=browser

)

async def main():
    # Run the agent
    history = await agent.run()
    result = history.final_result()
    print(result)
    # Close the browser
    await browser.close()
    input('Press Enter to exit...')
    


if __name__ == "__main__":
   
    asyncio.run(main())