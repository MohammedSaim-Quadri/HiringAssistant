def get_technical_prompt_with_context(experience, position, tech, difficulty="medium"):
    """
    Generate a technical question prompt based on the candidate's experience, position, technology,
    and desired difficulty level.

    Parameters:
        experience (int): Candidate's years of experience.
        position (str): The position the candidate is applying for.
        tech (str): The technology/tool/framework to base the question on.
        difficulty (str): Difficulty level of the question ('easy', 'medium', 'hard').

    Returns:
        str: The generated prompt for question creation.
    """
    experience_context = (
        "junior-level" if experience < 3 else 
        "mid-level" if experience < 7 else 
        "senior-level"
    )
    
    return (
        f"Generate a {difficulty} technical interview question suitable for a {experience_context} "
        f"candidate applying for the {position} position. The question should specifically test "
        f"practical knowledge of {tech}. If possible, include a real-world scenario. Respond only "
        f"with the question."
    )