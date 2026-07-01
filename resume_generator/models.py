from dataclasses import dataclass, field
from typing import List


@dataclass
class Skill:
    skill_name: str
    category: str
    proficiency: str
    years: float
    is_primary: bool


@dataclass
class Project:
    project_name: str
    client_name: str
    domain: str
    technology_stack: str
    role_name: str
    start_date: str
    end_date: str
    billing_status: str


@dataclass
class Certification:
    certification_name: str
    provider: str
    issue_date: str
    expiry_date: str
    status: str
    score: int


@dataclass
class Training:
    course_name: str
    provider: str
    technology: str
    completion_date: str
    score: int

@dataclass
class Resume:

    employee=None

    summary=""

    technical_skills=[]

    projects=[]

    certifications=[]

    trainings=[]



@dataclass
class Employee:

    employee_id: int

    first_name: str

    last_name: str

    email: str

    designation: str

    location: str

    experience_years: float

    domain: str

    joining_date: str

    utilization: str

    availability: str

    primary_skill: str = ""

    skills: List[Skill] = field(default_factory=list)

    projects: List[Project] = field(default_factory=list)

    certifications: List[Certification] = field(default_factory=list)

    trainings: List[Training] = field(default_factory=list)

    summary: str = ""