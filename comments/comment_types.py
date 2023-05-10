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
    CommentDeleted = 7
    CommentReacted = 8
    CommentUnReacted = 9

class CommentStrType(enum.StrEnum):
    ImageComment = "image"
    FileComment = "video"
    TEXT = "text"

class CommentTypesCommentMessage(TypedDict):
    comment: str
# class OutgoingEventBase(TypedDict):
#
class OutgoingCommentChangeReaction(NamedTuple):
    user:str
    commentId:str
    reactionType: str
    oldReaction: str
    newLikeNumber: int
    data_type: int = CommentTypes.CommentUnReacted
    type: str = "new_comment_changeReaction"
    def to_json(self) -> str:
        return json.dumps({
            "newLikeNumber": self.newLikeNumber,
            "oldReaction": self.oldReaction,
            "reactionType":self.reactionType,
            "commentId":self.commentId,
            "data_type": self.data_type,
            "type": self.type,
            "user": self.user
        })
class OutgoingCommentUnReacted(NamedTuple):
    user:str
    commentId:str
    oldReaction: str
    newLikeNumber: int
    data_type: int = CommentTypes.CommentUnReacted
    type: str = "new_comment_unreacted"
    def to_json(self) -> str:
        return json.dumps({
            "newLikeNumber": self.newLikeNumber,
            "reactionType":self.reactionType,
            "commentId":self.commentId,
            "data_type": self.data_type,
            "type": self.type,
            "user": self.user
        })
class OutgoingCommentReaction(NamedTuple):
    user:str
    commentId:str
    reactionType: str
    newLikeNumber: int
    data_type: int = CommentTypes.CommentReacted
    type: str = "new_comment_reacted"
    def to_json(self) -> str:
        return json.dumps({
            "newLikeNumber": self.newLikeNumber,
            "reactionType":self.reactionType,
            "commentId":self.commentId,
            "data_type": self.data_type,
            "type": self.type,
            "user": self.user
        })

class OutgoingEventCommentDeleted(NamedTuple):
    user: str
    commentId:str
    data_type: int = CommentTypes.CommentDeleted
    type: str = "new_comment_deleted"
    def to_json(self) -> str:
        return json.dumps({
            "commentId":self.commentId,
            "data_type":self.data_type,
            "type": self.type,
            "user":self.user
        })

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
