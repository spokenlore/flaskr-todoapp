CREATE TABLE IF NOT EXISTS user (
	username varchar(30) NOT NULL
	);

CREATE TABLE IF NOT EXISTS items(
	text varchar(30) NOT NULL,	
	status boolean,
    user_username varchar(30),
	FOREIGN KEY (user_username) references user(username)
	);
