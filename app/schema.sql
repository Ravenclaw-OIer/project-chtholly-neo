DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS class;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE class (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  teacher_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  current TEXT,
  namelist TEXT,
  FOREIGN KEY (teacher_id) REFERENCES user (id)
);
