CREATE DATABASE graphql_db; 

CREATE TABLE users (
    id INT NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(150),
    password VARCHAR(80)
);

ALTER TABLE users ADD PRIMARY KEY (id);
ALTER TABLE users MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1005;
