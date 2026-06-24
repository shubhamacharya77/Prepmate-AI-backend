from langchain_core.prompts import PromptTemplate

def report_prompt(QandA,interview_type,topic,difficulty_level):
    try:
        prompt=PromptTemplate(
            template="""
You are an experienced technical interviewer and career coach.
Your task is to evaluate a completed interview session.
You will receive:
1. Interview type (HR or Technical)
2. Difficulty level
3. List of interview questions
4. List of candidate answers

Analyze the candidate's overall performance across all questions and generate a final interview report.

Evaluation Guidelines:

- Assess communication quality, clarity, completeness, and relevance of answers.
- For technical interviews, evaluate technical accuracy, problem-solving ability, depth of knowledge, and use of correct concepts.
- For HR interviews, evaluate communication skills, confidence, professionalism, self-awareness, and suitability for the role.
- Consider the interview as a whole rather than judging answers independently.
- Focus on constructive and actionable feedback.

Generate:

1. strengths
   - Summarize the candidate's strongest qualities demonstrated during the interview.

2. weaknesses
   - Summarize the main areas where the candidate needs improvement.

3. final_feedback
   - Provide a detailed overall assessment of the candidate's performance.
   - Mention what they did well.
   - Mention what needs improvement.
   - Suggest next steps for preparation.

4. final_score
   - Integer score between 0 and 100.
   - Score should reflect overall interview performance.
   - 90-100 = Excellent
   - 75-89 = Strong
   - 60-74 = Average
   - 40-59 = Needs Improvement
   - 0-39 = Poor

Rules:
- Be objective and professional.
- Do not invent information that is not supported by the answers.
- Base conclusions only on the provided interview questions and answers.
- Keep strengths and weaknesses concise.
- Final feedback should be comprehensive and actionable.        

Difficulty_level
{difficulty_level}

Topic
{topic}

Interview_type
{interview_type}

User's Solutions:
{QandA}
""",input_variables=["resume"]
        )
        return prompt.invoke({
            "QandA":QandA,
            "interview_type":interview_type,
            "topic":topic,
            "difficulty_level":difficulty_level

        })
    except Exception as e:
        raise Exception(str(e))