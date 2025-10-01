I'm sorry, but as an AI text-based model, I don't have the capability to generate files or scripts. However, I can provide you with an example of how you can structure your SQL files for your automated testing system for BRICK 2. Please note that this is a simplified example and you may need to adjust it according to your specific needs.

1. Database schema definition:

```sql
CREATE DATABASE Brick2Testing;

USE Brick2Testing;

CREATE TABLE TestCases (
    TestCaseID int NOT NULL PRIMARY KEY,
    TestCaseName varchar(255) NOT NULL,
    Description varchar(1000),
    ExpectedResult varchar(1000) NOT NULL,
    CreationDate DATE NOT NULL
);

CREATE TABLE TestResults (
    ResultID int NOT NULL PRIMARY KEY,
    TestCaseID int NOT NULL,
    TestDate DATE NOT NULL,
    Result varchar(255) NOT NULL,
    FOREIGN KEY (TestCaseID) REFERENCES TestCases(TestCaseID)
);
```

2. Migration scripts:

```sql
-- This is a simple example of a migration script that adds a new column to the TestCases table
ALTER TABLE TestCases ADD COLUMN Priority varchar(255);
```

3. Seed data:

```sql
-- Inserting some test data
INSERT INTO TestCases (TestCaseID, TestCaseName, Description, ExpectedResult, CreationDate) 
VALUES (1, 'Test 1', 'This is test case 1', 'Pass', '2022-01-01');
```

4. Indexes and constraints:

```sql
-- Creating an index on the TestCaseName column
CREATE INDEX idx_TestCaseName ON TestCases (TestCaseName);

-- Adding a NOT NULL constraint to the Priority column
ALTER TABLE TestCases MODIFY COLUMN Priority varchar(255) NOT NULL;
```

5. Relationships:

```sql
-- The relationship between the TestCases and TestResults tables is defined in the TestResults table's foreign key constraint
```

I hope this example helps you in creating the actual SQL files for your system. You'd need to use an SQL client to run these files.