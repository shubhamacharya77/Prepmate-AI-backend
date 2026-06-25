from fastapi import APIRouter, status, HTTPException, Depends
from service.jwt_token import get_current_user
from service.database_operations import fetch_interview_by_id, fetch_QandAs, fetch_interview_report

router = APIRouter(prefix="/api")

@router.get("/interview_details/{interview_id}", tags=["Interview"])

def get_interview_details(interview_id: int, user=Depends(get_current_user)):
    try:
        # Fetch the base interview
        interview = fetch_interview_by_id(interview_id)
        if not interview:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found")
        
        # Verify ownership
        if interview.user_id != user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this interview")

        # Fetch Questions and Answers
        q_and_a_records = fetch_QandAs(interview_id)
        qa_list = []
        for record in q_and_a_records:
            qa_list.append({
                "id": record.id,
                "question": record.question,
                "answer": record.answer,
                "created_at": record.created_at
            })

        # Fetch the Report if it exists
        report_record = fetch_interview_report(interview_id)
        report_data = None
        if report_record:
            report_data = {
                "strengths": report_record.strengths,
                "weaknesses": report_record.weaknesses,
                "final_feedback": report_record.final_feedback,
                "final_score": report_record.final_score
            }

        return {
            "interview": {
                "id": interview.id,
                "title": interview.title,
                "difficulty_level": interview.difficulty_level,
                "interviews_type": interview.interviews_type,
                "status": interview.status,
                "created_at": interview.created_at
            },
            "q_and_a": qa_list,
            "report": report_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
