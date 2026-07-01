from resume_generator.data_loader import DataLoader
from resume_generator.resume_builder import ResumeBuilder
from resume_generator.pdf_generator import PDFGenerator


def main():

    loader = DataLoader()

    employees = loader.load_employees()

    builder = ResumeBuilder()

    pdf = PDFGenerator()

    resume = builder.build_resume(employees[0])
    output = pdf.generate(resume)

    print("=" * 60)
    print("Resume Generated Successfully")
    print("=" * 60)
    print(output)

    loader.close()


if __name__ == "__main__":
    main()