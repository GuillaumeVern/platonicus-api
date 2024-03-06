CREATE TABLE Player(
   Id_Player INT AUTO_INCREMENT,
   Name VARCHAR(50)  NOT NULL,
   PRIMARY KEY(Id_Player)
);

CREATE TABLE Score(
   Id_Score INT AUTO_INCREMENT,
   Score INT NOT NULL,
   Id_Player INT NOT NULL,
   PRIMARY KEY(Id_Score),
   FOREIGN KEY(Id_Player) REFERENCES Player(Id_Player)
);
