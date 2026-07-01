"""
===========================================================
Resume Builder
Creates resume content from Employee object
===========================================================
"""
from .templates import ResumeTemplates
import random
from collections import defaultdict


class ResumeBuilder:

    def build_resume(self, employee):
        """
        Returns a dictionary containing all resume sections.
        """

        return {
            "header": self.build_header(employee),
            "summary": self.build_summary(employee),
            "technical_skills": self.build_skills(employee),
            "projects": self.build_projects(employee),
            "certifications": self.build_certifications(employee),
            "trainings": self.build_trainings(employee),
            "education": self.build_education(employee),
            "achievements": self.build_achievements(employee)
        }

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    def build_header(self, employee):

        return {
            "employee_id": employee.employee_id,
            "name": f"{employee.first_name} {employee.last_name}",
            "designation": employee.designation,
            "email": employee.email,
            "location": employee.location,
            "experience": employee.experience_years,
            "domain": employee.domain
        }

    # --------------------------------------------------------
    # Professional Summary
    # --------------------------------------------------------

    def build_summary(self, employee):

        top_skills = [
            skill.skill_name
            for skill in employee.skills[:5]
        ]

        skills = ", ".join(top_skills)

        return (
            f"{employee.designation} with "
            f"{employee.experience_years} years of experience "
            f"in {employee.domain} domain. "
            f"Strong expertise in {skills}. "
            f"Experienced in enterprise application development, "
            f"Agile methodologies, REST API development and scalable software solutions."
        )

    # --------------------------------------------------------
    # Technical Skills
    # --------------------------------------------------------

    def build_skills(self, employee):

        grouped = defaultdict(list)

        for skill in employee.skills:

            grouped[skill.category].append({
                "skill": skill.skill_name,
                "level": skill.proficiency,
                "experience": skill.years,
                "primary": skill.is_primary
            })

        return dict(grouped)

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    def build_projects(self, employee):

        projects = []

        for project in employee.projects:

            responsibilities = self.generate_responsibilities(
                project.role_name,
                project.technology_stack
            )

            projects.append({

                "project_name": project.project_name,

                "client": project.client_name,

                "domain": project.domain,

                "role": project.role_name,

                "technology": project.technology_stack,

                "duration": f"{project.start_date} - {project.end_date}",

                "billing_status": project.billing_status,

                "responsibilities": responsibilities

            })

        return projects

    # --------------------------------------------------------
    # Certifications
    # --------------------------------------------------------

    def build_certifications(self, employee):

        certs = []

        for cert in employee.certifications:

            certs.append({

                "name": cert.certification_name,

                "provider": cert.provider,

                "issue_date": cert.issue_date,

                "expiry_date": cert.expiry_date,

                "status": cert.status,

                "score": cert.score

            })

        return certs

    # --------------------------------------------------------
    # Trainings
    # --------------------------------------------------------

    def build_trainings(self, employee):

        trainings = []

        for training in employee.trainings:

            trainings.append({

                "course": training.course_name,

                "provider": training.provider,

                "technology": training.technology,

                "completion_date": training.completion_date,

                "score": training.score

            })

        return trainings

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    def build_education(self, employee):

     passing_year = (
        2025 - int(employee.experience_years) - 4
    )

     return [

        {

            "degree": ResumeTemplates.random_degree(),

            "branch": ResumeTemplates.random_branch(),

            "university": ResumeTemplates.random_university(),

            "passing_year": passing_year

        }

    ] 

    # --------------------------------------------------------
    # Achievements
    # --------------------------------------------------------

    def build_achievements(self, employee):

     achievements = []

     if employee.experience_years >= 8:

         achievements.extend(
             ResumeTemplates.SENIOR_RESPONSIBILITIES[:3]
         )

     elif employee.experience_years >= 4:

         achievements.extend(
             ResumeTemplates.MID_RESPONSIBILITIES[:3]
         )

     else:

         achievements.extend(
             ResumeTemplates.JUNIOR_RESPONSIBILITIES[:3]
         )

     achievements.extend(

         random.sample(
             ResumeTemplates.ACHIEVEMENTS,
             3
         )

     )

     return achievements

    # --------------------------------------------------------
    # Responsibilities Generator
    # --------------------------------------------------------

    def generate_responsibilities(self, role, technology_stack):

        responsibilities = []
    
        role = role.lower()
    
        if "lead" in role or "architect" in role:
        
            responsibilities.extend(
                ResumeTemplates.SENIOR_RESPONSIBILITIES
            )
    
        elif "senior" in role:
        
            responsibilities.extend(
                ResumeTemplates.MID_RESPONSIBILITIES
            )
    
        else:
        
            responsibilities.extend(
                ResumeTemplates.JUNIOR_RESPONSIBILITIES
            )
    
        return responsibilities[:6]