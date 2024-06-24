from fastapi import APIRouter
from zb_msc_classificator.config.definition \
    import ConfigGeneral, ConfigEntityLinking
from zb_msc_classificator.api.data_models import Text, EntityData

from zb_msc_classificator.entity_linking import EntityLink

config = ConfigGeneral()
router = APIRouter()
el = EntityLink(config=ConfigEntityLinking())


@router.post(path="/entity_linking")
async def test(text: Text):
    return [
        EntityData(**item)
        for item in el.execute(text.text)
    ]

