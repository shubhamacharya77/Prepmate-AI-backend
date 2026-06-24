from langchain_core.messages import SystemMessage, HumanMessage

def get_roadmap_prompt(resume_jd_analysis: dict) -> list:
    system_prompt = """You are an expert career counselor and technical mentor.
Your task is to analyze the provided Candidate Resume vs Job Description analysis report and generate a comprehensive, structured, month-by-month career roadmap.

The user wants to bridge their skill gaps and reach their target goal. 
Based on the `matched_skills`, `missing_skills`, `experience_gap`, and other insights in the report, create a structured roadmap.

Your output must be a fully detailed roadmap, spanning enough months to realistically cover the gaps (e.g., 3 to 6 months depending on the gap size).
For each month, provide:
1. "month": The month identifier (e.g., "Month 1", "Month 2").
2. "topics": A high-level summary of the core topics to cover (e.g., "Python + ML").
3. "details": A detailed explanation of what to study, what projects to build, and why it is important for achieving their goal.

Ensure that the roadmap is actionable, progressive (builds upon previous months), and directly addresses the missing skills and recommendations from the analysis.
"""
    
    human_prompt = f"""
Here is the Resume vs JD Analysis Report:
{resume_jd_analysis}

Please generate the structured career roadmap.
"""
    return [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

