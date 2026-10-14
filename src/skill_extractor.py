def extract_skill(text, skills):
    found_skills= []

    for skill in skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills        
