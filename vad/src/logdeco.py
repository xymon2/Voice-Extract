import logging
import asyncio
import urllib.parse

logger = logging.getLogger("[VAD-MAIN]")

def log(func):
    async def wrap_log_async(*args, **kwargs):
        if args and hasattr(args[0], '__class__'):
            instance = args[0]
            class_name = instance.__class__.__name__
        else:
            class_name = "NonClass"
        
        request = args[1]
        func_name = func.__name__

        logger.info(f"START-CLASS:{class_name}-METHOD:{func_name}-BODY:{request}")
        result = await func(*args, **kwargs)
        logger.info(f"END-CLASS:{class_name}-METHOD:{func_name}-RESULT:{result}")
        return result

    def wrap_log_sync(*args, **kwargs):
        if args and hasattr(args[0], '__class__'):
            instance = args[0]
            class_name = instance.__class__.__name__
        else:
            class_name = "NonClass"
        
        request = args[1]
        func_name = func.__name__

        logger.info(f"START-CLASS:{class_name}-METHOD:{func_name}-BODY:{request}")
        result = func(*args, **kwargs)
        logger.info(f"END-CLASS:{class_name}-METHOD:{func_name}-RESULT:{result}")
        return result

    if asyncio.iscoroutinefunction(func):
        return wrap_log_async
    else:
        return wrap_log_sync