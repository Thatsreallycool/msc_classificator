from zb_msc_classificator.api.routes import router
from zb_msc_classificator.config.definition import ConfigGeneral
from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    placeholder for future extensions (running separate applications with
    different settings or different versions
    :return: app
    """
    config = ConfigGeneral()

    app = FastAPI(
        root_path=config.admin_config.api_config.root_path
    )
    app.include_router(router)

    return app
