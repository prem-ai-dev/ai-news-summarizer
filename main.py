from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
import time
from app.routers import ai_service_router

app=FastAPI()

@app.middleware("http")
async def check_point(request: Request,call_next):
    start_time=time.time()
    try:
        response= await call_next(request)
        process_time= time.time() - start_time
        response.headers["X-process-time"]=str(process_time)
        return response
    except Exception as e:
        print(f"unhandled error has occured as {e}")

        return JSONResponse(status_code=500,content={"details":type(e).__name__})

app.include_router(ai_service_router.router)