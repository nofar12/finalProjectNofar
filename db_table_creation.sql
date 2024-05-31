CREATE TABLE "reviews" (
	"reviewID"	INTEGER,
	"recipeID"	INTEGER NOT NULL,
	"reviewContent"	TEXT,
	"userID"	INTEGER,
	"time"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("userID") REFERENCES "users"("id"),
	PRIMARY KEY("reviewID" AUTOINCREMENT)
);

CREATE TABLE "sessions" (
	"session_id"	TEXT,
	"user_id"	INTEGER,
	"creation_timestamp"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"expiration_timestamp"	TIMESTAMP,
	PRIMARY KEY("session_id")
	FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE "users" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"profile_filename"	varchar(255) DEFAULT '/static/profilePicture.png',
	"salt"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "users_likes" (
	"interactionID"	INTEGER,
	"userID"	INTEGER,
	"recipeID"	TEXT NOT NULL,
	"time"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("userID") REFERENCES "users"("id"),
	UNIQUE("userID","recipeID"),
	PRIMARY KEY("interactionID" AUTOINCREMENT)
)
