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


class ChatPageTypes(enum.IntEnum):
    SyncPage = 1


# class OutgoingEventBase(TypedDict):
#

class OutgoingEventMessageRead(NamedTuple):
    message_id: int
    sender: str
    type: str = "message_read"

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.MessageRead,
            "message_id": self.message_id,
            "sender": self.sender,
        })

class UpdatePageEvents(NamedTuple):
    page:int
    def to_json(self) -> str:
        return json.dumps({
            "page":self.page
        })

class OutgoingEventNewTextMessage(NamedTuple):
    id: int
    username: str
    message_body: str
    sender: str
    receiver: str

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.TextMessage,
            "id": self.id,
            "message_body": self.message_body,
            "sender": self.sender,
        })


class OutgoingEventNewFileMessage(NamedTuple):
    id: int
    file: str
    sender: str
    message_type: int = MessageTypes.MessageRead

    def to_json(self) -> str:
        return json.dumps({
            "message_type": self.message_type,
            "db_id": self.id,
            "file": self.file,
            "sender": self.sender,
        })


class OutgoingEventNewUnreadCount(NamedTuple):
    sender: str
    unread_count: int
    type: str = "new_unread_count"

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.NewUnreadCount,
            "sender": self.sender,
            "unread_count": self.unread_count,
        })


class OutgoingEventMessageIdCreated(NamedTuple):
    id: int
    db_id: int
    type: str = "message_id_created"

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.MessageIdCreated,
            "id": self.id,
            "db_id": self.db_id,
        })


class OutgoingEventIsTyping(NamedTuple):
    user_pk: str
    type: str = "is_typing"

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.IsTyping,
            "user_pk": self.user_pk
        })


class OutgoingEventStoppedTyping(NamedTuple):
    user_pk: str
    type: str = "stopped_typing"

    def to_json(self) -> str:
        return json.dumps({
            "message_type": MessageTypes.TypingStopped,
            "user_pk": self.user_pk
        })
