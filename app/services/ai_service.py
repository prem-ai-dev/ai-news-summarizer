from google.genai import types,errors
import asyncio
from app.services.ai_tools import tool_functions, tool_declarations
from app.schemas.enum import Retry

class AiService:
    def __init__(self,ai):
        self.ai=ai

    async def news_summaraizer(self,content:str):
        temp_history=[]
        message={"role":"user","parts":[{"text":content}]}
        temp_history.append(message)
        for attempt in range(Retry.max_tries.value):
            try:
                while True:
                    response= await self.ai.aio.models.generate_content(
                                        model="gemini-3.1-flash-lite",
                                        contents=temp_history,
                                        config=types.GenerateContentConfig(
                                            system_instruction="""you are an news summarizer. You have
                                            tools to use according to user needs. You can have general greeting to user
                                            but anything beyond news respond with an refusal""",
                                            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                                            tools=[tool_declarations]
                                        )
                        )

                    if response.function_calls:
                        tasks=[]
                        for call in response.function_calls:
                            func=tool_functions.get(call.name)
                            tasks.append(func(**call.args))

                        results=await asyncio.gather(*tasks)

                        final_result=[]
                        for result,call in zip(results,response.function_calls):
                            final_result.append(types.Part.from_function_response(
                                                            name=call.name,
                                                            response=result
                                ))

                        temp_history.append({"role":"model","parts":response.candidates[0].content.parts})
                        temp_history.append({"role":"function","parts":final_result})

                    else:
                        async for chunk in await self.ai.aio.models.generate_content_stream(
                                            model="gemini-3.1-flash-lite",
                                            contents=temp_history,
                                            config=types.GenerateContentConfig(
                                            system_instruction="""you are an news summarizer.
                                            You can have general greeting to user but anything
                                            beyond news respond with an refusal""",
                                                                )
                            ):
                            yield f"event: message\ndata: {chunk.text}\n\n"
                        return

            except errors.ClientError as e:
                if e.code == 429:
                    wait= 2 ** attempt
                    await asyncio.sleep(wait)
                    continue
                yield f"data: ERROR: {e.message}\n\n"
                return
            except errors.ServerError as e:
                yield f"data: ERROR: {e.message}\n\n"
                return
            except ValueError as e:
                yield f"data: ERROR: {e}\n\n"
                return
            except asyncio.CancelledError:
                return
            except Exception as e:
                yield f"data: ERROR: {e}\n\n"
                return
        yield f"data: ERROR: service unavailable, please try again later\n\n"