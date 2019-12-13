# Database documentation
## Diagram 
![Diagram](https://github.com/jjjjm/Tsoha-RecipeDatabase/blob/master/documentation/current_db_diagram.png)
## Create table queries
```sql
CREATE TABLE recipe (
	id SERIAL NOT NULL, 
	name VARCHAR(144) NOT NULL, 
	instructions TEXT, 
	picture BYTEA, 
	PRIMARY KEY (id)
)

```
```sql
CREATE TABLE ingredient (
	id SERIAL NOT NULL, 
	name VARCHAR(144) NOT NULL, 
	measurement_unit VARCHAR(144), 
	PRIMARY KEY (id)
)

```
```sql
CREATE TABLE users (
	id SERIAL NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	admin BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
)

```
```sql
CREATE TABLE ingredient_user (
	ingredient_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	amount FLOAT NOT NULL, 
	PRIMARY KEY (ingredient_id, user_id), 
	FOREIGN KEY(ingredient_id) REFERENCES ingredient (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
)

```
```sql
CREATE TABLE recipe_ingredient (
	recipe_id INTEGER NOT NULL, 
	ingredient_id INTEGER NOT NULL, 
	amount FLOAT, 
	PRIMARY KEY (recipe_id, ingredient_id), 
	FOREIGN KEY(recipe_id) REFERENCES recipe (id) ON DELETE CASCADE, 
	FOREIGN KEY(ingredient_id) REFERENCES ingredient (id) ON DELETE CASCADE
)

```