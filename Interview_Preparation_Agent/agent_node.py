from Interview_Preparation_Agent.agent_state import agnetstate
from service.database_operations import *
from service.models import primary_llm
from prompts.Q_generation_prompt import Q_generation_prompt
from prompts.report_prompt import report_prompt
from service.request_schema import FinalInterviewReportSchema,QListSchema
from langgraph.types import interrupt
def fetch_context(state:agnetstate):
    try:
        #fetch resume details
        resume=fetch_resume(state.user_id)
        if resume:
            return{
                "resume_context":resume.model_dump()
            }
        else:
            return {
                "resume_context":None
            }
    except Exception as e:
        raise Exception(str(e))


def generate_questions(state:agnetstate):
    try:
        prompt=Q_generation_prompt(state.resume_context,state.interview_type,state.title,state.difficulty_level)
        model=primary_llm.with_structured_output(QListSchema)
        response=model.invoke(prompt)
        return{
            "generated_questions":[q.model_dump() for q in response.questions]
        }
    except Exception as e:
        raise Exception(str(e))
    
def interrupt_node(state:agnetstate):
        interrupt({
        "message": "waiting... for user input..."
    })
        return {}

def checknode(state:agnetstate):
    try:
        if state.count>=10:
            return "report_node"
        else:
            return "question_node"
    except Exception as e:
        raise Exception(str(e))

def get_question(state:agnetstate):
    try:
        current_count=state.count
        questions=state.generated_questions
        if current_count < len(questions):
            question = questions[current_count]
            answer_payload = interrupt({
                "question": question
            })
            
            full_qa = {
                "interview_id": state.interview_id,
                "question": question["question"],
                "answer": answer_payload["answer"],
                "interview_type": question["type"]
            }
            
            return {
                "Q_and_A": full_qa
            }
        return {}
    except Exception as e:
        raise Exception(str(e))
    
def store_answer(state:agnetstate):
    try:
        store_Q_and_A_in_db(state.Q_and_A.model_dump())
        return{
            "count":state.count+1
        }
    except Exception as e:
        raise Exception(str(e))

def report_node(state:agnetstate):
    try:
        QandAs=fetch_QandAs(state.interview_id)
        prompt=report_prompt(QandAs,state.interview_type,state.title,state.difficulty_level)
        model=primary_llm.with_structured_output(FinalInterviewReportSchema)
        report=model.invoke(prompt)
        
        report_data = report.model_dump()
        report_data["interview_id"] = state.interview_id
        store_report_in_db(report_data)
        
        # Change the interview status to Complete
        update_interview_status(state.interview_id, "Complete")
        
        return{
            "report":report
        }
    except Exception as e:
        raise Exception(str(e))