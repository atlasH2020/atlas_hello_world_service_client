--This file is just for reference. SQLAlchemy uses the models.py file to create the tables.


DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS user_services;
DROP TABLE IF EXISTS user_tokens;
DROP TABLE IF EXISTS services_registration;
DROP TABLE IF EXISTS oauth2_grant_code_flow_state;

-- #### postgres version #### ---
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_services(
  service_id TEXT NOT NULL,
  user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
  service_name TEXT NOT NULL,
  user_token_id INTEGER REFERENCES user_tokens(user_token_id),
  PRIMARY KEY(service_id, user_id)
);

CREATE TABLE user_tokens(
  user_token_id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  refresh_token TEXT,
  access_token TEXT,
  access_token_expires_in TEXT,
  refresh_token_expires_in TEXT,
  registration_id INTEGER NOT NULL REFERENCES services_registration(registration_id),
  UNIQUE (user_id, registration_id)
);


CREATE TABLE services_registration(
  registration_id SERIAL PRIMARY KEY,
  authorization_service_URL URL NOT NULL,
  client_id TEXT NOT NULL,
  client_secret TEXT NOT NULL,
  UNIQUE (authorization_service_URL)
);

CREATE TABLE oauth2_grant_code_flow_state(
  state_id TEXT PRIMARY KEY,
  service_id TEXT NOT NULL,
  service_name TEXT NOT NULL,
  oauth2_auth_url TEXT NOT NULL,
  oauth2_token_url TEXT NOT NULL
);