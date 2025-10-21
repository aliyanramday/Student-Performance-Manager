CREATE DATABASE StudentPerformanceDB;
USE StudentPerformanceDB;
CREATE TABLE SystemAccessors (
    AccessorID INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);
CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    MiddleName VARCHAR(255) NOT NULL,
    Photo VARCHAR(255)
) AUTO_INCREMENT = 101;
CREATE TABLE Subjects (
    SubjectCode VARCHAR(10) PRIMARY KEY,
    SubjectName VARCHAR(255) NOT NULL
);
CREATE TABLE StudentGrades (
    StudentID INT,
    SubjectCode VARCHAR(10),
    Term INT CHECK (term BETWEEN 1 AND 3),
    Grade FLOAT CHECK (Grade BETWEEN 0 AND 100),
    PRIMARY KEY (StudentID, SubjectCode, Term),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (SubjectCode) REFERENCES Subjects(SubjectCode) ON DELETE CASCADE
);
INSERT INTO SystemAccessors (AccessorID, Email, Password) VALUES 
('1', 'admin@school.com', 'securePass123');
INSERT INTO Students (StudentID, FirstName, MiddleName, Photo) VALUES 
(101, 'Alice', 'Johnson', '/Users/aliyanaliramday/Desktop/OOPS\ ASS/1.jpeg'),
(102, 'David', 'Smith', '/Users/aliyanaliramday/Desktop/OOPS\ ASS/2.jpeg'),
(103, 'Emma', 'Brown', '/Users/aliyanaliramday/Desktop/OOPS\ ASS/3.png'),
(104, 'Michael', 'Williams', '/Users/aliyanaliramday/Desktop/OOPS\ ASS/4.jpeg'),
(105, 'Sophia', 'Davis', '/Users/aliyanaliramday/Desktop/OOPS\ ASS/5.jpeg');
INSERT INTO Subjects (SubjectCode, SubjectName) VALUES 
('CS1OOP', 'Object Oriented Programming'),
('CS1CS', 'Computer Systems'),
('MTY9MP0001', 'Maths');
INSERT INTO StudentGrades (StudentID, SubjectCode, Term, Grade) VALUES 
(101, 'CS1OOP', 1, 85.5),
(101, 'CS1CS', 1, 78.0),
(101, 'MTY9MP0001', 1, 92.3),
(102, 'CS1OOP', 2, 75.6),
(102, 'CS1CS', 3, 87.2),
(102, 'MTY9MP0001', 3, 88.9),
(103, 'CS1OOP', 2, 89.4),
(103, 'CS1CS', 3, 78.3),
(103, 'MTY9MP0001', 3, 84.1),
(104, 'CS1OOP', 3, 88.0),
(104, 'CS1CS', 2, 92.5),
(104, 'MTY9MP0001', 3, 80.4),
(105, 'CS1OOP', 3, 91.7),
(105, 'CS1CS', 1, 90.2),
(105, 'MTY9MP0001', 3, 87.3);
