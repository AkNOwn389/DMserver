





import enum














class PostType(enum.StrEnum):
    POST = "posts"
    NEWSPOST = "news"
    POSTIMAGE = "postImage"
    VIDEO = "videos"


class PostReactionType(enum.StrEnum):
    LIKE = "Like"
    LOVE = "Love"
    HAPPY = "Happy"
    WOW = "Wow"
    ANGRY = "Angry"
    SAD = "Sad"


class ReactOrUnReact(enum.StrEnum):
    REACT = "react"
    UNREACT = "unReact"