from langchain_core.prompts import PromptTemplate

def analysis_prompt(detaild_jd:str):
    try:
        prompt=PromptTemplate(
            template="""
You are an expert Technical Recruiter, Hiring Manager, and ATS Specialist.
Your task is to analyze a Job Description (JD) and extract all relevant hiring requirements into a structured format.

Instructions:

1. Carefully read the entire Job Description.
2. Extract information exactly as stated in the JD.
3. Do not hallucinate or invent information.
4. If information is missing, return null or an empty list as appropriate.
5. Separate mandatory requirements from preferred requirements whenever possible.
6. Normalize skill names and technologies into commonly used industry terms.
7. Extract both technical and non-technical requirements.
8. Capture years of experience only when explicitly mentioned.
9. Preserve important business context and domain information.
10. Focus on information useful for candidate screening, ATS matching, interview preparation, and skill-gap analysis.

Extraction Requirements:

- Job Title
- Required Skills (Tools and Technologies)

Rules:

- Required skills should contain only mandatory skills.
- Preferred skills should contain optional or bonus skills.
- Tools and technologies should include frameworks, libraries, cloud platforms, databases, programming languages, and software tools.
- Responsibilities should be concise and actionable.
- Do not place responsibilities inside skills.
- Do not place skills inside responsibilities.
- Extract the exact minimum experience requirement whenever available.
- Extract degree and specialization requirements whenever available.
- Industry domain should represent the business sector (e.g., Healthcare, FinTech, EdTech, E-Commerce, SaaS, Banking, Insurance, Recruitment).

Output must strictly follow the provided structured schema.
Do not return explanations, markdown, commentary, or additional text.
Return only the structured output.

Job Description:

{Detailed_JD}
""",input_variables=["Detailed_JD"]
        )
        return prompt.invoke({
            "Detailed_JD":detaild_jd
        })
    except Exception as e:
        raise Exception(str(e))