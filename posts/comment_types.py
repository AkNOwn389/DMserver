import enum
import json
from chats.models import UploadedFile

# TODO: add tx_id to distinguish errors for different transactions
from typing import NamedTuple, Optional, Dict, List, Any

try:
    from typing import TypedDict
except ImportError:
    TypedDict = dict


try:
    from typing import TypedDict
except ImportError:
    TypedDict = dict

class CommentTypes(enum.IntEnum):
    CommentMessage = 1
    FileComment = 2
    ErrorOccurred = 3
    CommentCreated = 4
    IsTyping = 5
    StopTyping = 6

class CommentTypesCommentMessage(TypedDict):
    comment: str
# class OutgoingEventBase(TypedDict):
#

class OutgoingEventIsTyping(NamedTuple):
    user: str
    data_type: int = CommentTypes.IsTyping
    type: str = "user_typing"
    def to_json(self) -> str:
        return json.dumps({
            "data_type": self.data_type,
            "type": self.type,
            "user": self.user
        })


class OutgoingEventStoppedTyping(NamedTuple):
    user: str
    data_type: int = CommentTypes.StopTyping
    type: str = "user_stop_typing"
    def to_json(self) -> str:
        return json.dumps({
            "data_type": self.data_type,
            "type":self.type,
            "user": self.user
        })
