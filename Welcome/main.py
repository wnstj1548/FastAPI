from fastapi import FastAPI

app = FastAPI()

@app.get("/",
         summary="간단한 API",
         tags=["Simple"])
async def root():
    '''

    이것은 간단한 API 입니다. 아래는 인자값입니다.

    - **인자값1은 이거고여
    - **인자값2는 이거입니다.

    '''
    return {"message": "Hello World"}