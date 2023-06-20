import logging
import asyncio
import urllib.parse

logger = logging.getLogger("sanic.root")
# logger.setLevel(logging.DEBUG)

def httplog(func):
    async def wrap_log_async(*args, **kwargs):
        if args and hasattr(args[0], '__class__'):
            instance = args[0]
            class_name = instance.__class__.__name__
        else:
            class_name = "NonClass"
        
        request = args[1]

        base_path = urllib.parse.urlparse(request.url).path
        query_params = urllib.parse.parse_qs(request.query_string)
        query_params_str = urllib.parse.urlencode(query_params, doseq=True)
        combined_path = base_path
        if query_params_str:
            combined_path += "?" + query_params_str

        method = request.method
        func_name = func.__name__
        body = request.body.decode()

        logger.info(f"START-{method} {combined_path}-CLASS:{class_name}-METHOD:{func_name}-BODY:{body}")
        result = await func(*args, **kwargs)
        logger.info(f"END-{method} {combined_path}-CLASS:{class_name}-METHOD:{func_name}-RESULT:{result}")
        return result

    def wrap_log_sync(*args, **kwargs):
        if args and hasattr(args[0], '__class__'):
            instance = args[0]
            class_name = instance.__class__.__name__
        else:
            class_name = "NonClass"
        request = args[1]

        base_path = urllib.parse.urlparse(request.url).path
        query_params = urllib.parse.parse_qs(request.query_string)
        query_params_str = urllib.parse.urlencode(query_params, doseq=True)
        combined_path = base_path
        if query_params_str:
            combined_path += "?" + query_params_str

        method = request.method
        func_name = func.__name__
        body = request.body.decode()

        logger.info(f"START-{method} {combined_path}-CLASS:{class_name}-METHOD:{func_name}-BODY:{body}")
        result = func(*args, **kwargs)
        logger.info(f"END-{method} {combined_path}-CLASS:{class_name}-METHOD:{func_name}-RESULT:{result}")
        return result

    if asyncio.iscoroutinefunction(func):
        return wrap_log_async
    else:
        return wrap_log_sync