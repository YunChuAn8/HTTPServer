from fastapi import FastAPI
from pydantic import BaseModel
import random
import time
import asyncio
import math
import uvicorn

app = FastAPI()

#BaseModel被用作数据验证和设置的基础,该模型具有的特定的字段和类型将在处理请求时自动验证。
class NumberRequest(BaseModel):
    number: int

@app.post("/sqrt")
async def sqrt(request: NumberRequest):
    ##如果请求体中的数据与NumberRequest的定义不匹配，FastAPI将返回一个HTTP 422错误，指出验证失败。
    number = request.number
    delay = random.uniform(0.1, 0.19)
    await asyncio.sleep(delay)
    result = math.sqrt(number)
    return {"result": result, "delay": delay}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
