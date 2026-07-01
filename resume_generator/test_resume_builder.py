from resume_generator.data_loader import DataLoader
from resume_generator.resume_builder import ResumeBuilder

loader = DataLoader()
employees = loader.load_employees()

builder = ResumeBuilder()

resume = builder.build_resume(employees[0])

print("=" * 60)
print(resume["header"])
print("=" * 60)
print(resume["summary"])
print("=" * 60)
print(resume["technical_skills"])
print("=" * 60)
print("Projects:", len(resume["projects"]))
print("Certifications:", len(resume["certifications"]))
print("Trainings:", len(resume["trainings"]))

loader.close()