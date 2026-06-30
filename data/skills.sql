-- ==========================================
-- Seed Data : skills
-- ==========================================

INSERT INTO skills (skill_name, category, description, active)
VALUES

-- ===========================
-- Backend
-- ===========================
('Java', 'Backend', 'Java Programming Language', TRUE),
('Spring Boot', 'Backend', 'Spring Boot Framework', TRUE),
('Hibernate', 'Backend', 'ORM Framework', TRUE),
('Microservices', 'Backend', 'Microservices Architecture', TRUE),
('REST API', 'Backend', 'RESTful Web Services', TRUE),
('Kafka', 'Backend', 'Apache Kafka', TRUE),
('Maven', 'Backend', 'Build Tool', TRUE),
('JUnit', 'Backend', 'Unit Testing Framework', TRUE),
('Node.js', 'Backend', 'Node.js Runtime', TRUE),
('Express.js', 'Backend', 'Express Framework', TRUE),
('Python', 'Backend', 'Python Programming', TRUE),
('Django', 'Backend', 'Django Framework', TRUE),
('FastAPI', 'Backend', 'FastAPI Framework', TRUE),
('Flask', 'Backend', 'Flask Framework', TRUE),
('.NET Core', 'Backend', '.NET Core Framework', TRUE),
('C#', 'Backend', 'C# Programming Language', TRUE),

-- ===========================
-- Frontend
-- ===========================
('React', 'Frontend', 'React JS', TRUE),
('Angular', 'Frontend', 'Angular Framework', TRUE),
('Vue.js', 'Frontend', 'Vue Framework', TRUE),
('TypeScript', 'Frontend', 'TypeScript Language', TRUE),
('JavaScript', 'Frontend', 'JavaScript Language', TRUE),
('HTML5', 'Frontend', 'HTML5', TRUE),
('CSS3', 'Frontend', 'CSS3', TRUE),
('Bootstrap', 'Frontend', 'Bootstrap Framework', TRUE),
('Tailwind CSS', 'Frontend', 'Tailwind CSS', TRUE),
('Redux', 'Frontend', 'Redux State Management', TRUE),
('Next.js', 'Frontend', 'Next.js Framework', TRUE),

-- ===========================
-- Cloud
-- ===========================
('AWS', 'Cloud', 'Amazon Web Services', TRUE),
('Azure', 'Cloud', 'Microsoft Azure', TRUE),
('Google Cloud', 'Cloud', 'Google Cloud Platform', TRUE),
('OpenShift', 'Cloud', 'RedHat OpenShift', TRUE),

-- ===========================
-- DevOps
-- ===========================
('Docker', 'DevOps', 'Docker Containers', TRUE),
('Kubernetes', 'DevOps', 'Container Orchestration', TRUE),
('Terraform', 'DevOps', 'Infrastructure as Code', TRUE),
('Ansible', 'DevOps', 'Configuration Management', TRUE),
('Jenkins', 'DevOps', 'CI/CD Tool', TRUE),
('GitHub Actions', 'DevOps', 'CI/CD Pipeline', TRUE),
('Helm', 'DevOps', 'Kubernetes Package Manager', TRUE),

-- ===========================
-- Database
-- ===========================
('PostgreSQL', 'Database', 'PostgreSQL Database', TRUE),
('MySQL', 'Database', 'MySQL Database', TRUE),
('Oracle', 'Database', 'Oracle Database', TRUE),
('MongoDB', 'Database', 'MongoDB NoSQL', TRUE),
('SQL Server', 'Database', 'Microsoft SQL Server', TRUE),
('Redis', 'Database', 'Redis Cache', TRUE),

-- ===========================
-- Data Engineering
-- ===========================
('Apache Spark', 'Data Engineering', 'Distributed Processing', TRUE),
('Hadoop', 'Data Engineering', 'Big Data Framework', TRUE),
('Airflow', 'Data Engineering', 'Workflow Scheduler', TRUE),
('Databricks', 'Data Engineering', 'Lakehouse Platform', TRUE),
('Snowflake', 'Data Engineering', 'Cloud Data Warehouse', TRUE),

-- ===========================
-- AI / GenAI
-- ===========================
('Prompt Engineering', 'AI', 'Prompt Design', TRUE),
('LangChain', 'AI', 'LLM Framework', TRUE),
('LangGraph', 'AI', 'Agent Framework', TRUE),
('RAG', 'AI', 'Retrieval Augmented Generation', TRUE),
('MCP', 'AI', 'Model Context Protocol', TRUE),
('ChromaDB', 'AI', 'Vector Database', TRUE),
('FAISS', 'AI', 'Vector Search Library', TRUE),
('Pinecone', 'AI', 'Managed Vector Database', TRUE),
('OpenAI API', 'AI', 'OpenAI API Integration', TRUE),
('Azure OpenAI', 'AI', 'Azure OpenAI Service', TRUE),

-- ===========================
-- Testing
-- ===========================
('Selenium', 'Testing', 'UI Automation', TRUE),
('Playwright', 'Testing', 'Modern UI Automation', TRUE),
('JUnit Testing', 'Testing', 'Java Testing', TRUE),
('Postman', 'Testing', 'API Testing', TRUE),
('JMeter', 'Testing', 'Performance Testing', TRUE),

-- ===========================
-- Mobile
-- ===========================
('Android', 'Mobile', 'Android Development', TRUE),
('Kotlin', 'Mobile', 'Kotlin Language', TRUE),
('Flutter', 'Mobile', 'Flutter Framework', TRUE),
('React Native', 'Mobile', 'Cross Platform Mobile', TRUE),
('Swift', 'Mobile', 'iOS Development', TRUE),

-- ===========================
-- Salesforce
-- ===========================
('Salesforce', 'CRM', 'Salesforce Platform', TRUE),
('Apex', 'CRM', 'Apex Programming', TRUE),
('Lightning Web Components', 'CRM', 'LWC Development', TRUE),
('SOQL', 'CRM', 'Salesforce Query Language', TRUE);