from service.database import get_local_session
from service.database_schema import Resume_table
from sqlmodel import select

def get_raw_resume_txt_from_DB(user_id) ->dict:
    try:
        with get_local_session() as db:
            resume = db.exec(
                select(Resume_table)
                .where(Resume_table.user_id == user_id)
            ).first()

            if not resume:
                raise ValueError(f"No resume found for user_id={user_id}")

            return {
                "id":resume.id,
                "text":resume.resume_raw_txt
            }

    except Exception as e:
        raise Exception(str(e))

