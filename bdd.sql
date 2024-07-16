CREATE TABLE app_user(
   id_user INT AUTO_INCREMENT,
   username VARCHAR(50)  NOT NULL,
   password VARCHAR(50)  NOT NULL,
   email VARCHAR(50) ,
   PRIMARY KEY(id_user)
);

CREATE TABLE player(
   id_player INT AUTO_INCREMENT,
   pseudo VARCHAR(50)  NOT NULL,
   id_user INT NOT NULL,
   PRIMARY KEY(id_player),
   FOREIGN KEY(id_user) REFERENCES app_user(id_user)
);

CREATE TABLE score(
   id_score INT AUTO_INCREMENT,
   score INT NOT NULL,
   id_player INT NOT NULL,
   PRIMARY KEY(id_score),
   FOREIGN KEY(id_player) REFERENCES player(id_player)
);

CREATE TABLE token(
   token VARCHAR(50)  NOT NULL,
   id_user INT NOT NULL,
   PRIMARY KEY(token),
   FOREIGN KEY(id_user) REFERENCES app_user(id_user)
);