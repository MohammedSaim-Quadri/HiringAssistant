def get_technical_prompt_with_context(experience, position, tech):
    return (
        f"Generate a technical interview question suitable for a candidate applying for the "
        f"{position} position with {experience} years of experience. The question should "
        f"specifically test practical knowledge of {tech}. Respond only with the question."
    )
