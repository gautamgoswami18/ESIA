-- ==========================================
-- Seed Data : Certifications
-- ==========================================

INSERT INTO esia.certifications
(certification_id, certification_name, vendor, validity_years)
VALUES

-- ===========================
-- AWS
-- ===========================
(1, 'AWS Certified Cloud Practitioner', 'AWS', 3),
(2, 'AWS Certified Developer - Associate', 'AWS', 3),
(3, 'AWS Certified Solutions Architect - Associate', 'AWS', 3),
(4, 'AWS Certified DevOps Engineer - Professional', 'AWS', 3),

-- ===========================
-- Microsoft Azure
-- ===========================
(5, 'Microsoft Certified: Azure Fundamentals (AZ-900)', 'Microsoft', 0),
(6, 'Microsoft Certified: Azure Administrator (AZ-104)', 'Microsoft', 2),
(7, 'Microsoft Certified: Azure Developer Associate (AZ-204)', 'Microsoft', 2),
(8, 'Microsoft Certified: Azure AI Engineer Associate (AI-102)', 'Microsoft', 2),

-- ===========================
-- Google Cloud
-- ===========================
(9, 'Associate Cloud Engineer', 'Google', 2),
(10, 'Professional Cloud Architect', 'Google', 2),

-- ===========================
-- Oracle
-- ===========================
(11, 'Oracle Certified Professional Java SE 17 Developer', 'Oracle', 5),
(12, 'Oracle Database SQL Certified Associate', 'Oracle', 5),

-- ===========================
-- Kubernetes / CNCF
-- ===========================
(13, 'Certified Kubernetes Administrator (CKA)', 'CNCF', 3),
(14, 'Certified Kubernetes Application Developer (CKAD)', 'CNCF', 3),

-- ===========================
-- Red Hat
-- ===========================
(15, 'Red Hat Certified System Administrator (RHCSA)', 'Red Hat', 3),
(16, 'Red Hat Certified Engineer (RHCE)', 'Red Hat', 3),

-- ===========================
-- Scrum / Agile
-- ===========================
(17, 'Certified Scrum Master (CSM)', 'Scrum Alliance', 2),
(18, 'Professional Scrum Master I (PSM I)', 'Scrum.org', 0),
(19, 'PMI Agile Certified Practitioner (PMI-ACP)', 'PMI', 3),

-- ===========================
-- DevOps
-- ===========================
(20, 'HashiCorp Certified Terraform Associate', 'HashiCorp', 2),
(21, 'Docker Certified Associate', 'Docker', 2),
(22, 'Jenkins Engineer Certification', 'CloudBees', 2),

-- ===========================
-- Salesforce
-- ===========================
(23, 'Salesforce Certified Administrator', 'Salesforce', 3),
(24, 'Salesforce Platform Developer I', 'Salesforce', 3),
(25, 'Salesforce Platform App Builder', 'Salesforce', 3),

-- ===========================
-- Data Engineering
-- ===========================
(26, 'Databricks Certified Data Engineer Associate', 'Databricks', 2),
(27, 'SnowPro Core Certification', 'Snowflake', 2),

-- ===========================
-- AI / GenAI
-- ===========================
(28, 'Microsoft Azure AI Engineer Associate', 'Microsoft', 2),
(29, 'OpenAI API Developer Certification', 'OpenAI', 2),
(30, 'LangChain Developer Certification', 'LangChain', 2);