from resume_generator.data_loader import DataLoader


def main():

    loader = DataLoader()

    employees = loader.load_employees()

    print("=" * 60)
    print("Employees Loaded :", len(employees))
    print("=" * 60)

    emp = employees[0]

    print()

    print("Employee :", emp.first_name, emp.last_name)

    print("Primary Skill :", emp.primary_skill)

    print("Skills :", len(emp.skills))

    print("Projects :", len(emp.projects))

    print("Certifications :", len(emp.certifications))

    print("Training :", len(emp.trainings))

    loader.close()


if __name__ == "__main__":
    main()