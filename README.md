# HTTPServer
实现一个高延迟的API，并创建客户端程序进行功能验证和性能压测。其中提供了两版API方案。  
**两种方案**：  
**1. Nginx （反向代理）+ Gunicorn（WSGI服务器） + Flask （Web应用框架）**  
Nginx将客户端的请求转发给后端的Gunicorn服务器，Gunicorn接收转发过来的请求，并调用Flask应用进行处理。  
**2. Nginx （反向代理）+Uvicorn（ASGI服务器）+FastAPI（web框架）**  
Uvicorn 是一个基于 ASGI 的服务器，专门用于处理异步 Python Web 应用程序。  
