import logging
from service.database import get_local_session
from fastapi import HTTPException,status,Depends
from service.database_schema import *
from sqlmodel import select
from service.supabase_init import delete_resume_supabase
from service.vectorstore import delete_resume_vector


def fetch_user(user_id:int):
    try:
        with get_local_session() as db:
            user=db.exec(select(User_table).where(User_table.id==user_id)).first()
            if user:
                return user
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found !")
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def uploadResumeDatabase(user_id:int,resume_name:str,supabase_details:dict,raw_text:str):
    try:
        with get_local_session() as db:
            resume_DB=Resume_table(
            user_id=user_id,
            resume_name=resume_name,
            resume_raw_txt=raw_text,
            resume_path=supabase_details["storage"].path# use the explicitly constructed full path
        )

            db.add(resume_DB)
            db.commit()
            db.refresh(resume_DB)
        return resume_DB
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    
def deleteResumeDatabase(resume):
    try:
        if not resume:
            return
        with get_local_session() as db:
            db_resume = db.exec(select(Resume_table).where(Resume_table.id == resume.id)).first()
            if db_resume:
                analysis = db.exec(select(Resume_analysis_table).where(Resume_analysis_table.resume_id == db_resume.id)).first()
                if analysis:
                    db.delete(analysis)

                roadmap = db.exec(select(Career_Roadmap_table).where(Career_Roadmap_table.user_id == db_resume.user_id)).first()
                if roadmap:
                    db.delete(roadmap)

                jd_analysis = db.exec(select(ResumeJDAnalysis_table).where(ResumeJDAnalysis_table.user_id == db_resume.user_id)).first()
                if jd_analysis:
                    db.delete(jd_analysis)

                db.delete(db_resume)
                db.commit()
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))



def fetch_resume(user_id:int):
    try:
        with get_local_session() as db:
            resume=db.exec(select(Resume_table).where(Resume_table.user_id==user_id)).first()
            return resume
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def fetch_resume_analysis_by_user(user_id:int):
    try:
        with get_local_session() as db:
            resume = db.exec(select(Resume_table).where(Resume_table.user_id == user_id)).first()
            if not resume:
                return None
            analysis = db.exec(select(Resume_analysis_table).where(Resume_analysis_table.resume_id == resume.id)).first()
            return analysis
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def fetch_readmap(user_id:int):
    try:
        with get_local_session() as db:
            roadmap=db.exec(select(Career_Roadmap_table).where(Career_Roadmap_table.user_id==user_id)).first()
            if roadmap :
                return roadmap
            else:
                return None
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def store_road_map(data:dict):
    try:
        with get_local_session() as DB:
                roadmap_record = Career_Roadmap_table(
                    resume_id=data["resume_id"],
                    user_id=data["user_id"],
                    goal=data["roadmap"]["goal"],
                    roadmap=data["roadmap"]
                )
                DB.add(roadmap_record)
                DB.commit()
                DB.refresh(roadmap_record)
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))


def store_resume_analysis(data):
    try:
        with get_local_session() as DB:
            analysis_record=Resume_analysis_table(
                resume_id=data["resume_id"],
                skills=data["skills"],
                experience=data["experience"],
                projects=data["projects"],
                education=data["education"],
                summary=data["summary"],
            )
            DB.add(analysis_record)
            DB.commit()
            DB.refresh(analysis_record)
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def store_resume_report(data):
    try:
        with get_local_session() as DB:
            analysis_record=ResumeJDAnalysis_table(
                resume_id=data["resume_id"],
                user_id=data["user_id"],
                match_score=data["match_score"],
                matched_skills=data["matched_skills"],
                missing_skills=data["missing_skills"],
                additional_skills=data["additional_skills"],
                experience_match=data["experience_match"],
                required_experience=data["required_experience"],
                candidate_experience=data["candidate_experience"],
                experience_gap=data["experience_gap"],
                relevant_projects=data["relevant_projects"],
                missing_project_domains=data["missing_project_domains"],
                strengths=data["strengths"],
                weaknesses=data["weaknesses"],
                recommendations=data["recommendations"],
                ats_keywords_found=data["ats_keywords_found"],
                ats_keywords_missing=data["ats_keywords_missing"],
                summary=data["summary"]
            )
            DB.add(analysis_record)
            DB.commit()
            DB.refresh(analysis_record)
        
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def fetch_interviews(user_id:int):
    try:
        with get_local_session() as db:
            interviews=db.exec(select(Interviews_table).where(Interviews_table.user_id==user_id)).all()
            if interviews:
                return interviews
            else:
                return None
            
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def fetch_interview_by_id(interview_id:int):
    try:
        with get_local_session() as db:
            interview = db.exec(select(Interviews_table).where(Interviews_table.id == interview_id)).first()
            return interview
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def fetch_interview_report(interview_id:int):
    try:
        with get_local_session() as db:
            report = db.exec(select(final_interview_report).where(final_interview_report.interview_id == interview_id)).first()
            return report
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def delete_user_interview(id:int):
    try:
        with get_local_session() as db:
            interview = db.exec(select(Interviews_table).where(Interviews_table.id == id)).first()
            if interview:
                db.delete(interview)
                db.commit()
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def delete_user_interview_history(interview_id:int):
    try:
        with get_local_session() as db:
            qandas = db.exec(select(QandA).where(QandA.interview_id == interview_id)).all()
            for qa in qandas:
                db.delete(qa)

            reports = db.exec(select(final_interview_report).where(final_interview_report.interview_id == interview_id)).all()
            for report in reports:
                db.delete(report)

            db.commit()
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def delete_resume_report(user_id:int):
    # resumeJDanalysis-report
    try:
        with get_local_session() as db:
            report = db.exec(select(ResumeJDAnalysis_table).where(ResumeJDAnalysis_table.user_id == user_id)).first()
            if report:
                db.delete(report)
                db.commit()
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))


def delete_user_data(user_id:int):
    try:
        with get_local_session() as db:
            user = db.exec(select(User_table).where(User_table.id == user_id)).first()
            if not user:
                return

            resume = db.exec(select(Resume_table).where(Resume_table.user_id == user_id)).first()
            if resume:
                analysis = db.exec(select(Resume_analysis_table).where(Resume_analysis_table.resume_id == resume.id)).first()
                if analysis:
                    db.delete(analysis)

                roadmap = db.exec(select(Career_Roadmap_table).where(Career_Roadmap_table.user_id == user_id)).first()
                if roadmap:
                    db.delete(roadmap)

                jd_analysis = db.exec(select(ResumeJDAnalysis_table).where(ResumeJDAnalysis_table.user_id == user_id)).first()
                if jd_analysis:
                    db.delete(jd_analysis)

                if resume.resume_path:
                    delete_resume_supabase(resume.resume_path)
                delete_resume_vector(user_id)
                db.delete(resume)

            interviews = db.exec(select(Interviews_table).where(Interviews_table.user_id == user_id)).all()
            for interview in interviews:
                qandas = db.exec(select(QandA).where(QandA.interview_id == interview.id)).all()
                for qa in qandas:
                    db.delete(qa)

                reports = db.exec(select(final_interview_report).where(final_interview_report.interview_id == interview.id)).all()
                for report in reports:
                    db.delete(report)

                db.delete(interview)

            db.delete(user)
            db.commit()
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))


def delete_user_in_db(user_id:int):
    try:
        with get_local_session() as db:
            user=db.exec(select(User_table).where(User_table.id==user_id)).first()
            db.delete(user)
            db.commit()
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    

def create_interview_in_db(data:dict):
    try:
        with get_local_session() as db:
            new_interview=Interviews_table(
                user_id=data["id"],
                title=data["title"],
                difficulty_level=data["difficulty_level"],
                interviews_type=data["interviews_type"],
                status=data["status"]
            )
            db.add(new_interview)
            db.commit()
            db.refresh(new_interview)
            return new_interview.id
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def fetch_active_interview(user_id:int):
    try:
        with get_local_session() as db:
            Interview=db.exec(select(Interviews_table).where(Interviews_table.user_id == user_id,Interviews_table.status =="Start")).first()
            return Interview
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def store_Q_and_A_in_db(data:dict):
    try:
        with get_local_session() as db:
            new_QandA=QandA(
                interview_id=data["interview_id"],
                interview_type=data["interview_type"],
                question=data["question"],
                answer=data["answer"]
            )
            db.add(new_QandA)
            db.commit()
            db.refresh(new_QandA)
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))
    
def fetch_QandAs(interview_id:int):
    try:
        with get_local_session() as db:
            QandAs=db.exec(select(QandA).where(QandA.interview_id == interview_id)).all()
            return QandAs
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def store_report_in_db(data:dict):
    try:
        with get_local_session() as db:
            report=final_interview_report(
                interview_id=data["interview_id"],
                strengths=data["strengths"],
                weaknesses=data["weaknesses"],
                final_feedback=data["final_feedback"],
                final_score=data["final_score"]
            )
            db.add(report)
            db.commit()
            db.refresh(report)
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

def update_interview_status(interview_id: int, status: str):
    try:
        with get_local_session() as db:
            interview = db.exec(select(Interviews_table).where(Interviews_table.id == interview_id)).first()
            if interview:
                interview.status = status
                db.add(interview)
                db.commit()
                db.refresh(interview)
    except Exception as e:
        logging.error("Database operation failed", exc_info=True)
        raise Exception(str(e))

