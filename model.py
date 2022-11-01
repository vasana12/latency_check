from typing import Optional, List
from datetime import datetime
from pytz import timezone
from pydantic import BaseModel, Field
from pydantic.datetime_parse import parse_datetime

class utc_datetime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime  # default pydantic behavior
        yield cls.convert_kst

    @classmethod
    def convert_kst(cls, v):
        # if TZ isn't provided, we assume UTC, but you can do w/e you need

        if v.tzinfo == timezone("UTC"):
            return v.astimezone(timezone("Asia/Seoul")).replace(tzinfo=None)
        return v.replace(tzinfo=None)



class MediaCreateSchema(BaseModel):
    """data-schema when user create media(post media)"""
    content:str

class Media(BaseModel):
    username: str
    content: str
    created_at: utc_datetime = Field(default=utc_datetime.now())

class MediaListSchema(BaseModel):
    total_count:int
    media_list:List[Media]

if __name__ == "__main__":
    media = Media(**{"username": "test", "content": "content_test"})
    print(media)


