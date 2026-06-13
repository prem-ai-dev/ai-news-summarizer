import httpx
import asyncio
from google.genai import types,errors
from app.schemas.enum import Retry
from app.core.ai import client
from app.schemas.sentiment_schema import SentimentSchema
from app.core.config import access

async def fetch_news(content:str):
    """fetch news details. always get the topic from user"""

    for attempt in range(Retry.max_tries.value):
        try:
            async with httpx.AsyncClient() as http_client:
                response= await http_client.get(
                    url="https://newsapi.org/v2/everything",
                    params={"q":content,
                            "language": "en",
                            "apikey":f"{access.NEW_API_KEY}"}
                )

                if response.status_code == 200:
                    fn_result={}
                    data=response.json()
                    article=data.get("articles",[])
                    if article:
                        first=article[0]
                        fn_result["author"]=first.get("author","unknown")
                        fn_result["description"]=first.get("description")
                        fn_result["source_url"]=first.get("url")

                        print("api_done")
                        return {"result":fn_result}

                return {"error": "cannot be connected at the moment. Try again"}
        except (httpx.RequestError, httpx.TimeoutException):
            wait = 2 ** attempt
            await asyncio.sleep(wait)
            continue
    return {"error":"cannot connect with api"}

async def get_sentiment(content:str):
    """Analyze the sentiment of a given news text.
    Call this after fetching news to determine if the sentiment is positive, negative, or neutral."""
    for attempt in range(Retry.max_tries.value):
        try:
            response= await client.aio.models.generate_content(
                                model="gemini-2.5-flash-lite",
                                contents=content,
                                config=types.GenerateContentConfig(
                                    system_instruction="""provide the sentiment for given prompt.
                                    Do reply for anything beyond sentiment finding""",
                                    response_schema=SentimentSchema
                                )
            )
            result=response.text
            print("sentiment_done")
            return {"result":result}

        except errors.ClientError as e:
            if e.code == 429:
                wait = 2 ** attempt
                await asyncio.sleep(wait)
                continue
            return {"error":e.message}
        except errors.ServerError as e:
            return {"error":e.message}
        except ValueError as e:
            return {"error":str(e)}
        except Exception as e:
            return {"error":str(e)}
    return {"error":"max retries exceeded"}

tool_functions={
            "fetch_news":fetch_news,
            "get_sentiment":get_sentiment
}

tool_declarations=types.Tool(function_declarations=[
            types.FunctionDeclaration.from_callable(client=client, callable=fetch_news),
            types.FunctionDeclaration.from_callable(client=client, callable=get_sentiment)
])