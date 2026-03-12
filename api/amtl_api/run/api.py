from fastapi import FastAPI

# from uvicorn.config import LOGGING_CONFIG
from amtl_api.adapters.api import api_settings, run_app
from amtl_api.adapters.api.config import logger
from amtl_api.adapters.api.lifespan import lifespan

app = run_app(
    app=FastAPI(
        lifespan=lifespan,
        title=f"API: {api_settings.API_NAME}, v{api_settings.API_VER}"
    )
)

if __name__ == "__main__":
    import uvicorn

    args_dict: dict = {
        "host": api_settings.API_HOST,
        "port": api_settings.API_PORT,
        "log_level": api_settings.UVICORN_LOG_LEVEL,
    }

    if api_settings.IS_DEBUG is True:
        args_dict["reload"] = True
    else:
        args_dict["workers"] = api_settings.API_WORKERS
        
    logger.info(f"Start app with {args_dict}")

    uvicorn.run(
        "__main__:app",
        **args_dict
    )
