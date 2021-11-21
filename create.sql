DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Item;

CREATE TABLE Item(
    "ItemID" INTEGER not null, 
    "Name" VARCHAR(255) not null,
    "Category" VARCHAR(255) not null,
    "Num_Category" INTEGER not null,
    "Currently" DECIMAL,
    "First_Bid" DECIMAL,
    "Number_of_Bids" DECIMAL not null,
    "Location" VARCHAR(255) not null,
    Country VARCHAR(255) not null,
    Started TIME not null,
    Ends TIME not null,
    Seller VARCHAR(255) not null,
    Buy_Price DECIMAL,
    Description TEXT not null,
    PRIMARY KEY(ItemID),
    FOREIGN KEY(Seller) REFERENCES User(UserID)
);

CREATE TABLE User(
    UserID VARCHAR(255) NOT NULL,
    Rating INTEGER NOT NULL,
    Location VARCHAR(255),
    Country VARCHAR(255),
    PRIMARY KEY(UserID)
);

CREATE TABLE Bid(
    UserID VARCHAR(255) NOT NULL,     
    ItemID INTEGER NOT NULL,    
    Time DATETIME NOT NULL,
    Amount DECIMAL,
    PRIMARY KEY(UserID, ItemID),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Category(
    ItemID INTEGER not null,
    Category VARCHAR(255) not null,
    PRIMARY KEY(Category, ItemID),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)
);
