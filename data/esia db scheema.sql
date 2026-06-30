-- ============================================================
-- Employee Skill Intelligence Assistant
-- Schema Creation Script
-- PostgreSQL 16+
-- ============================================================

CREATE SCHEMA IF NOT EXISTS esia;

SET search_path TO esia;

---------------------------------------------------------------
-- MANAGERS
---------------------------------------------------------------

CREATE TABLE managers (

    manager_id          SERIAL PRIMARY KEY,

    manager_code        VARCHAR(20) UNIQUE NOT NULL,

    first_name          VARCHAR(100) NOT NULL,

    last_name           VARCHAR(100) NOT NULL,

    email               VARCHAR(200) UNIQUE NOT NULL,

    designation         VARCHAR(100),

    location            VARCHAR(100),

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---------------------------------------------------------------
-- SKILLS
---------------------------------------------------------------

CREATE TABLE skills (

    skill_id            SERIAL PRIMARY KEY,

    skill_name          VARCHAR(100) UNIQUE NOT NULL,

    category            VARCHAR(50) NOT NULL,

    description         TEXT,

    active              BOOLEAN DEFAULT TRUE
);

---------------------------------------------------------------
-- EMPLOYEES
---------------------------------------------------------------

CREATE TABLE employees (

    employee_id         SERIAL PRIMARY KEY,

    employee_code       VARCHAR(20) UNIQUE NOT NULL,

    first_name          VARCHAR(100) NOT NULL,

    last_name           VARCHAR(100) NOT NULL,

    email               VARCHAR(200) UNIQUE NOT NULL,

    phone               VARCHAR(20),

    designation         VARCHAR(100),

    location            VARCHAR(100),

    experience_years    NUMERIC(4,1),

    manager_id          INTEGER,

    primary_skill_id    INTEGER,

    domain              VARCHAR(100),

    utilization         INTEGER CHECK(utilization BETWEEN 0 AND 100),

    availability        VARCHAR(50),

    joining_date        DATE,

    employment_status   VARCHAR(20) DEFAULT 'Active',

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_manager
        FOREIGN KEY(manager_id)
        REFERENCES managers(manager_id),

    CONSTRAINT fk_primary_skill
        FOREIGN KEY(primary_skill_id)
        REFERENCES skills(skill_id)
);

---------------------------------------------------------------
-- EMPLOYEE SKILLS
---------------------------------------------------------------

CREATE TABLE employee_skills (

    employee_skill_id       SERIAL PRIMARY KEY,

    employee_id             INTEGER NOT NULL,

    skill_id                INTEGER NOT NULL,

    proficiency_level       VARCHAR(20),

    years_of_experience     NUMERIC(4,1),

    is_primary              BOOLEAN DEFAULT FALSE,

    last_used               DATE,

    CONSTRAINT fk_emp_skill_employee
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_emp_skill_skill
        FOREIGN KEY(skill_id)
        REFERENCES skills(skill_id),

    CONSTRAINT uq_employee_skill
        UNIQUE(employee_id, skill_id)
);

---------------------------------------------------------------
-- PROJECTS
---------------------------------------------------------------

CREATE TABLE projects (

    project_id          SERIAL PRIMARY KEY,

    project_code        VARCHAR(20) UNIQUE,

    project_name        VARCHAR(200),

    client_name         VARCHAR(200),

    domain              VARCHAR(100),

    technology_stack    TEXT,

    start_date          DATE,

    end_date            DATE,

    project_status      VARCHAR(30)
);

---------------------------------------------------------------
-- EMPLOYEE PROJECTS
---------------------------------------------------------------

CREATE TABLE employee_projects (

    allocation_id           SERIAL PRIMARY KEY,

    employee_id             INTEGER NOT NULL,

    project_id              INTEGER NOT NULL,

    role_name               VARCHAR(100),

    allocation_percentage   INTEGER,

    billing_status          VARCHAR(30),

    start_date              DATE,

    end_date                DATE,

    CONSTRAINT fk_alloc_employee
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_alloc_project
        FOREIGN KEY(project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

---------------------------------------------------------------
-- CERTIFICATIONS
---------------------------------------------------------------

CREATE TABLE certifications (

    certification_id        SERIAL PRIMARY KEY,

    certification_name      VARCHAR(200),

    vendor                  VARCHAR(100),

    validity_years          INTEGER
);

---------------------------------------------------------------
-- EMPLOYEE CERTIFICATIONS
---------------------------------------------------------------

CREATE TABLE employee_certifications (

    employee_certification_id    SERIAL PRIMARY KEY,

    employee_id                 INTEGER,

    certification_id            INTEGER,

    issue_date                  DATE,

    expiry_date                 DATE,

    certification_status        VARCHAR(30),

    CONSTRAINT fk_emp_cert_employee
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_emp_cert_cert
        FOREIGN KEY(certification_id)
        REFERENCES certifications(certification_id)
);

---------------------------------------------------------------
-- RESUME METADATA
---------------------------------------------------------------

CREATE TABLE resume_metadata (

    resume_id           SERIAL PRIMARY KEY,

    employee_id         INTEGER UNIQUE,

    file_name           VARCHAR(300),

    file_path           VARCHAR(500),

    upload_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    version             INTEGER DEFAULT 1,

    embedding_status    BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_resume_employee
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE
);

---------------------------------------------------------------
-- TRAINING CATALOG
---------------------------------------------------------------

CREATE TABLE training_catalog (

    training_id         SERIAL PRIMARY KEY,

    course_name         VARCHAR(200),

    technology          VARCHAR(100),

    provider            VARCHAR(100),

    duration_hours      INTEGER,

    level               VARCHAR(50)
);

---------------------------------------------------------------
-- EMPLOYEE TRAINING
---------------------------------------------------------------

CREATE TABLE employee_training (

    employee_training_id    SERIAL PRIMARY KEY,

    employee_id             INTEGER,

    training_id             INTEGER,

    completion_status       VARCHAR(30),

    score                   NUMERIC(5,2),

    completion_date         DATE,

    CONSTRAINT fk_training_employee
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_training_catalog
        FOREIGN KEY(training_id)
        REFERENCES training_catalog(training_id)
);

---------------------------------------------------------------
-- AUDIT LOGS
---------------------------------------------------------------

CREATE TABLE audit_logs (

    audit_id            BIGSERIAL PRIMARY KEY,

    username            VARCHAR(100),

    action_name         VARCHAR(100),

    table_name          VARCHAR(100),

    record_id           INTEGER,

    action_timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    details             JSONB
);

---------------------------------------------------------------
-- END OF TABLES
---------------------------------------------------------------