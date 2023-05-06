import enum
import json

# TODO: add tx_id to distinguish errors for different transactions
from typing import NamedTuple, Optional, Dict

try:
    from typing import TypedDict
except ImportError:
    TypedDict = dict


class MessageTypeTextMessage(TypedDict):
    text: str
    user_pk: str
    id: int


class MessageTypeMessageRead(TypedDict):
    user_pk: str
    message_id: int


class MessageTypeFileMessage(TypedDict):
    file_id: str
    user_pk: str
    id: int


class MessageTypes(enum.IntEnum):
    WentOnline = 1
    WentOffline = 2
    TextMessage = 3
    FileMessage = 4
    IsTyping = 5
    MessageRead = 6
    ErrorOccurred = 7
    MessageIdCreated = 8
    NewUnreadCount = 9
    TypingStopped = 10
    RefreshPage = 11
    UpdatePage = 12
    DeleteMessage = 13
    ReactMessage = 14


class ChatPageTypes(enum.IntEnum):
    SyncPage = 1


# class OutgoingEventBase(TypedDict):
#

class OutgoingEventMessageRead(NamedTuple):
    id: int
    sender: str
    type: str = "message_read"

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.MessageRead,
            "message_id": self.message_id,
            "sender": self.sender,
        })

class OutgoingEventIsTyping(NamedTuple):
    user: str
    type: str = "is_typing"

    def to_json(self) -> str:
        return json.dumps({
            "type": self.type,
            "message_type": MessageTypes.IsTyping,
            "user": self.user
        })


class OutgoingEventStoppedTyping(NamedTuple):
    user: str
    type: str = "stopped_typing"

    def to_json(self) -> str:
        return json.dumps({
            "type": self.type,
            "message_type": MessageTypes.TypingStopped,
            "user": self.user
        })
