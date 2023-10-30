---------------------
-- CREATE DATABASE --
---------------------

CREATE DATABASE IF NOT EXISTS 'KuihDadar' DEFAULT CHARACTER SET utf8;
USE 'KuihDadar';

-------------------
-- CREATE TABLES --
-------------------

-- Create the Role table
CREATE TABLE Role (
    Role_Name VARCHAR(20) PRIMARY KEY,
    Role_Desc LONGTEXT NOT NULL
);

-- Create the Access_Rights table
CREATE TABLE Access_Rights (
    Access_ID INT PRIMARY KEY,
    Access_Control_Name VARCHAR(50) NOT NULL
);

-- Create the Skill table
CREATE TABLE Skill (
    Skill_Name VARCHAR(50) PRIMARY KEY,
    Skill_Desc LONGTEXT NOT NULL
);

-- Create the Staff table
CREATE TABLE Staff (
    Staff_ID INT PRIMARY KEY,
    Staff_FName VARCHAR(50) NOT NULL,
    Staff_LName VARCHAR(50) NOT NULL,
    Dept VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Access_ID INT,
    FOREIGN KEY (Access_ID) REFERENCES Access_Rights(Access_ID)
);

-- Create the Role_Skill table
CREATE TABLE Role_Skill (
    Role_Name VARCHAR(20),
    Skill_Name VARCHAR(50),
    FOREIGN KEY (Role_Name) REFERENCES Role(Role_Name),
    FOREIGN KEY (Skill_Name) REFERENCES Skill(Skill_Name)
);

-- Create the Staff_Skill table
CREATE TABLE Staff_Skill (
    Staff_ID INT,
    Skill_Name VARCHAR(50),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    FOREIGN KEY (Skill_Name) REFERENCES Skill(Skill_Name)
);

-- Create the Listings table
CREATE TABLE Listings (
    Listing_ID INT PRIMARY KEY,
    Role_Name VARCHAR(20),
    Opening_Date INT NOT NULL,
    Closing_Date INT NOT NULL,
    FOREIGN KEY (Role_Name) REFERENCES Role(Role_Name)
);

-- Create the Applications table
CREATE TABLE Applications (
    Application_ID INT PRIMARY KEY,
    ApplicationDate INT NOT NULL,
    Listing_ID INT,
    Staff_ID INT,
    FOREIGN KEY (Listing_ID) REFERENCES Listings(Listing_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);


