CREATE TABLE IF NOT EXISTS user (
	username varchar(30) primary key NOT NULL
	);

CREATE TABLE IF NOT EXISTS items(
	key int primary key NOT NULL AUTOINCREMENT,
	text varchar(30) NOT NULL,	
	status boolean,
    user_username varchar(30),
	FOREIGN KEY (user_username) references user(username)
	);
