"""
===========================================================
Resume Content Templates
===========================================================
"""

import random


class ResumeTemplates:

    # ---------------------------------------------------------
    # Professional Summary
    # ---------------------------------------------------------

    SUMMARY_TEMPLATES = [

        "{designation} with over {exp} years of experience in "
        "{domain} domain. Strong expertise in {skills}. "
        "Experienced in designing scalable enterprise applications "
        "and delivering high-quality software solutions using Agile methodologies.",

        "Highly motivated {designation} possessing {exp} years of "
        "industry experience in {domain}. Skilled in {skills}. "
        "Passionate about software engineering, cloud technologies "
        "and enterprise application development.",

        "Experienced {designation} specializing in {domain} domain "
        "with {exp} years of hands-on experience. "
        "Strong knowledge of {skills}. "
        "Committed to delivering reliable, scalable and maintainable software.",

        "{designation} with a proven track record of delivering "
        "enterprise solutions across the {domain} industry. "
        "Possesses {exp} years of experience with expertise in {skills}. "
        "Strong analytical and problem-solving abilities."
    ]

    # ---------------------------------------------------------
    # Junior Responsibilities
    # ---------------------------------------------------------

    JUNIOR_RESPONSIBILITIES = [

        "Developed application modules based on business requirements.",

        "Fixed production issues and resolved defects.",

        "Participated in Agile Scrum ceremonies.",

        "Developed REST APIs and reusable components.",

        "Collaborated with QA and business teams.",

        "Performed unit testing and code reviews."
    ]

    # ---------------------------------------------------------
    # Mid Level Responsibilities
    # ---------------------------------------------------------

    MID_RESPONSIBILITIES = [

        "Designed scalable backend services.",

        "Developed Microservices architecture.",

        "Optimized application performance.",

        "Integrated third-party APIs.",

        "Participated in architecture discussions.",

        "Mentored junior developers.",

        "Implemented CI/CD deployment pipelines."
    ]

    # ---------------------------------------------------------
    # Senior Responsibilities
    # ---------------------------------------------------------

    SENIOR_RESPONSIBILITIES = [

        "Led end-to-end software development lifecycle.",

        "Designed enterprise-grade system architecture.",

        "Mentored development teams.",

        "Collaborated with solution architects.",

        "Improved system scalability and reliability.",

        "Led technical design discussions.",

        "Delivered business-critical applications.",

        "Defined coding standards and best practices."
    ]

    # ---------------------------------------------------------
    # Achievements
    # ---------------------------------------------------------

    ACHIEVEMENTS = [

        "Successfully delivered enterprise applications within schedule.",

        "Recognized for technical excellence and problem solving.",

        "Hands-on experience working in Agile Scrum teams.",

        "Strong analytical and debugging capabilities.",

        "Excellent communication and stakeholder management.",

        "Experience working with distributed cross-functional teams.",

        "Contributed to performance optimization initiatives.",

        "Actively participated in knowledge sharing sessions."
    ]

    # ---------------------------------------------------------
    # Education
    # ---------------------------------------------------------

    UNIVERSITIES = [

        "Indian Institute of Technology",

        "National Institute of Technology",

        "Delhi Technological University",

        "VIT University",

        "SRM Institute of Science and Technology",

        "Anna University",

        "Mumbai University",

        "University of Pune",

        "AKTU",

        "JNTU Hyderabad"
    ]

    DEGREES = [

        "Bachelor of Technology",

        "Bachelor of Engineering",

        "Master of Computer Applications"
    ]

    BRANCHES = [

        "Computer Science",

        "Information Technology",

        "Electronics & Communication",

        "Software Engineering"
    ]

    # ---------------------------------------------------------
    # Helper Methods
    # ---------------------------------------------------------

    @staticmethod
    def random_summary():

        return random.choice(
            ResumeTemplates.SUMMARY_TEMPLATES
        )

    @staticmethod
    def random_university():

        return random.choice(
            ResumeTemplates.UNIVERSITIES
        )

    @staticmethod
    def random_degree():

        return random.choice(
            ResumeTemplates.DEGREES
        )

    @staticmethod
    def random_branch():

        return random.choice(
            ResumeTemplates.BRANCHES
        )