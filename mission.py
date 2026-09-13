def generate_application_mission(profile, opportunity):

    skills = profile.get("skills", [])
    title = opportunity.get("title", "this opportunity")
    matching_skills = opportunity.get("matching_skills", [])
    missing_requirements = opportunity.get("missing_requirements", [])
    reason = opportunity.get("reason", "")

    skill_text = ", ".join(skills)
    matching_text = ", ".join(matching_skills) if matching_skills else "your technical skills"

    if missing_requirements:
        missing_text = ", ".join(missing_requirements)
    else:
        missing_text = "No major missing requirements identified"

    match_summary = (
        f"This opportunity matches your goal of {profile.get('goal', 'career growth')}. "
        f"Your relevant skills include {matching_text}. "
        f"Overall assessment: {reason}"
    )

    resume_suggestions = [
        f"Highlight {matching_text} prominently in your technical skills section.",
        f"Emphasize your experience with {skill_text}.",
        f"Address the following requirement gaps where applicable: {missing_text}."
    ]

    cover_letter = (
        f"Dear Hiring Manager,\n\n"
        f"I am a 3rd-year CSE student interested in the {title} opportunity. "
        f"My technical skills include {skill_text}, and I am particularly interested "
        f"in building my experience in AI and software engineering. "
        f"This opportunity aligns well with my career goals, and I would be excited "
        f"to contribute while continuing to develop my technical skills. "
        f"I am available for opportunities in India or remotely.\n\n"
        f"Thank you for considering my application."
    )

    checklist = [
        "Review job requirements",
        "Tailor resume using the suggestions",
        "Review the generated cover letter",
        "Verify eligibility and application details",
        "Open the official application page"
    ]

    return {
        "match_summary": match_summary,
        "resume_suggestions": resume_suggestions,
        "cover_letter": cover_letter,
        "checklist": checklist
    }