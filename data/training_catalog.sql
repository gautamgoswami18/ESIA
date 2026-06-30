-- ==========================================
-- Seed Data : Training Catalog
-- ==========================================

INSERT INTO esia.training_catalog
(training_id, course_name, technology, provider, duration_hours, level)
VALUES

-- ===========================
-- Java
-- ===========================
(1, 'Java Fundamentals', 'Java', 'Internal Learning Portal', 24, 'Beginner'),
(2, 'Advanced Java Programming', 'Java', 'Internal Learning Portal', 32, 'Intermediate'),
(3, 'Spring Boot Microservices', 'Spring Boot', 'Udemy Business', 40, 'Advanced'),
(4, 'REST API Development', 'Java', 'Pluralsight', 16, 'Intermediate'),

-- ===========================
-- Frontend
-- ===========================
(5, 'React Fundamentals', 'React', 'Internal Learning Portal', 24, 'Beginner'),
(6, 'Advanced React & Redux', 'React', 'Udemy Business', 32, 'Advanced'),
(7, 'Angular Development', 'Angular', 'Pluralsight', 30, 'Intermediate'),
(8, 'Modern JavaScript & TypeScript', 'JavaScript', 'Coursera', 20, 'Intermediate'),

-- ===========================
-- Python
-- ===========================
(9, 'Python Programming', 'Python', 'Internal Learning Portal', 30, 'Beginner'),
(10, 'Advanced Python', 'Python', 'Coursera', 35, 'Advanced'),
(11, 'FastAPI Development', 'FastAPI', 'Udemy Business', 18, 'Intermediate'),

-- ===========================
-- Cloud
-- ===========================
(12, 'AWS Cloud Practitioner', 'AWS', 'AWS Skill Builder', 18, 'Beginner'),
(13, 'AWS Solutions Architect', 'AWS', 'AWS Skill Builder', 40, 'Advanced'),
(14, 'Microsoft Azure Fundamentals', 'Azure', 'Microsoft Learn', 16, 'Beginner'),
(15, 'Azure AI Engineer', 'Azure AI', 'Microsoft Learn', 32, 'Advanced'),
(16, 'Google Cloud Essentials', 'GCP', 'Google Cloud Skills Boost', 24, 'Intermediate'),

-- ===========================
-- DevOps
-- ===========================
(17, 'Docker Essentials', 'Docker', 'Internal Learning Portal', 16, 'Beginner'),
(18, 'Kubernetes Administration', 'Kubernetes', 'Linux Foundation', 40, 'Advanced'),
(19, 'Jenkins CI/CD', 'Jenkins', 'Pluralsight', 20, 'Intermediate'),
(20, 'Terraform Infrastructure as Code', 'Terraform', 'HashiCorp Learn', 24, 'Advanced'),

-- ===========================
-- Databases
-- ===========================
(21, 'PostgreSQL Administration', 'PostgreSQL', 'Internal Learning Portal', 24, 'Intermediate'),
(22, 'MongoDB for Developers', 'MongoDB', 'MongoDB University', 18, 'Intermediate'),
(23, 'Oracle SQL Programming', 'Oracle', 'Oracle University', 20, 'Intermediate'),

-- ===========================
-- Data Engineering
-- ===========================
(24, 'Apache Spark Fundamentals', 'Apache Spark', 'Databricks Academy', 32, 'Intermediate'),
(25, 'Databricks Data Engineering', 'Databricks', 'Databricks Academy', 40, 'Advanced'),
(26, 'Snowflake Fundamentals', 'Snowflake', 'Snowflake University', 20, 'Intermediate'),

-- ===========================
-- AI / Generative AI
-- ===========================
(27, 'Prompt Engineering for Developers', 'Generative AI', 'Internal Learning Portal', 12, 'Beginner'),
(28, 'LangChain Essentials', 'LangChain', 'Internal Learning Portal', 20, 'Intermediate'),
(29, 'LangGraph Agent Development', 'LangGraph', 'Internal Learning Portal', 24, 'Advanced'),
(30, 'Retrieval Augmented Generation (RAG)', 'Generative AI', 'Internal Learning Portal', 18, 'Advanced'),
(31, 'Model Context Protocol (MCP)', 'MCP', 'Internal Learning Portal', 12, 'Intermediate'),
(32, 'Vector Databases with ChromaDB', 'ChromaDB', 'Internal Learning Portal', 16, 'Intermediate'),
(33, 'OpenAI API Development', 'OpenAI', 'OpenAI Learning', 16, 'Intermediate'),

-- ===========================
-- Testing
-- ===========================
(34, 'Selenium Automation', 'Selenium', 'Udemy Business', 24, 'Intermediate'),
(35, 'API Testing with Postman', 'Postman', 'Postman Academy', 12, 'Beginner'),
(36, 'Performance Testing with JMeter', 'JMeter', 'Apache', 20, 'Intermediate'),

-- ===========================
-- Salesforce
-- ===========================
(37, 'Salesforce Administration', 'Salesforce', 'Trailhead', 24, 'Beginner'),
(38, 'Salesforce Platform Developer', 'Salesforce', 'Trailhead', 32, 'Advanced'),

-- ===========================
-- Agile & Leadership
-- ===========================
(39, 'Agile Scrum Fundamentals', 'Agile', 'Internal Learning Portal', 12, 'Beginner'),
(40, 'Technical Leadership Essentials', 'Leadership', 'Internal Learning Portal', 16, 'Advanced');