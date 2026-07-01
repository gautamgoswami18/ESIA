from resume_generator.data_loader import DataLoader
from resume_generator.resume_builder import ResumeBuilder
from resume_generator.pdf_generator import PDFGenerator


def main():

    print("=" * 70)
    print("ESIA Resume Generator")
    print("=" * 70)

    loader = DataLoader()
    employees = loader.load_employees()

    builder = ResumeBuilder()
    pdf_generator = PDFGenerator()

    success = 0
    failed = 0

    for employee in employees:

        try:
            resume = builder.build_resume(employee)

            pdf_path = pdf_generator.generate(resume)

            success += 1

            print(f"[{success:03}] Generated: {pdf_path.name}")

        except Exception as ex:

            failed += 1

            print(f"[ERROR] Employee {employee.employee_id} : {ex}")

    loader.close()

    print("\n" + "=" * 70)
    print(f"Total Employees : {len(employees)}")
    print(f"Generated       : {success}")
    print(f"Failed          : {failed}")
    print("=" * 70)


if __name__ == "__main__":
    main()