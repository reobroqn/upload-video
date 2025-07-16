from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.video import Video
from app.schemas.video_status import VideoStatus


def create_test_video(db: Session, user: User) -> Video:
    """Helper function to create a video for testing."""
    video = Video(
        title="Test Video",
        description="A video for testing purposes.",
        file_key=f"{user.id}/test_video.mp4",
        file_size=1024 * 1024,  # 1MB
        mime_type="video/mp4",
        status=VideoStatus.PENDING,
        owner_id=user.id,
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def test_confirm_upload_complete(
    client: TestClient,
    db: Session,
    test_user: tuple[User, str],
    user_token_headers: dict,
):
    """
    Test the /videos/upload-complete endpoint.
    """
    user, _ = test_user
    # 1. Create a video with 'pending' status
    video = create_test_video(db, user)
    assert video.status == VideoStatus.PENDING

    # 2. Call the upload-complete endpoint
    response = client.post(
        f"{settings.API_V1_STR}/videos/upload-complete",
        headers=user_token_headers,
        json={"video_id": video.id},
    )

    # 3. Assert the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == video.id
    assert data["status"] == "uploaded"

    # 4. Verify the status in the database is updated
    db.refresh(video)
    assert video.status == VideoStatus.UPLOADED
