from enum import Enum


class VideoStatus(str, Enum):
    """
    Enum for video processing status.
    """

    PENDING = "pending"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
