# Use cases and the SQL queries used in them
All ``?`` in queries represent parameters that are passed (with ``VALUES``) to mitigate SQL-injections
## User stories
### User can create an account 
    ```sql
    INSERT INTO users (username, password, admin) VALUES (?,?,?) RETURNING users.id
    ```
### User can login 
```sql
    SELECT users.id AS users_id, users.username AS users_username, users.password AS users_password, users.admin AS users_admin 
    FROM users 
    WHERE users.id = ?
```
### Site has admin accounts, with the ability to delete any row from any table and change admin status of users
```sql
    DELETE FROM x WHERE x.id = ? --Delete row, x can be users, recipe, ingredient. Changes cascade to fk tables.  
    UPDATE users SET admin= ? WHERE users.id = ? --Update admin status:
```
    
### User can keep track of their current cooking ingredient inventory. 
```sql
    SELECT Ingredient.id, Ingredient.name, Ingredient.measurement_unit, Ingredient_User.amount 
    FROM Ingredient 
    INNER JOIN Ingredient_User 
    ON Ingredient.id = Ingredient_User.ingredient_id 
    AND Ingredient_user.user_id = ?
```
### User can add new ingredients to their inventory 
```sql
    INSERT INTO ingredient_user (ingredient_id, user_id, amount) VALUES (?, ?, ?)
```
### User can add recipes to the recipe book 
```sql
    INSERT INTO recipe (name, instructions, picture) VALUES (?, ?, ?) RETURNING recipe.id
    INSERT INTO recipe_ingredient (recipe_id, ingredient_id, amount) VALUES (?, ?, ?) -- for each added ingredient
```
### User can see what recipes they can make with the ingredients they currently have 
```sql
     SELECT DISTINCT r.id as id ,r.name as name 
     FROM Recipe r 
     LEFT JOIN Recipe_Ingredient ri ON r.id = ri.recipe_id
     LEFT JOIN Ingredient_User iu ON ri.ingredient_id = iu.ingredient_id
     WHERE iu.user_id = 1 AND iu.amount >= ri.amount
     OR iu.amount IS NULL
```
### User can search recipes they can currently make by listing abstract ingredients / ingredients (no need to have them in inventory) 
```sql
    SELECT DISTINCT r.id as recipe_id, r.name as recipe_name, i.name as ingredient_name 
    FROM Recipe r 
    LEFT JOIN Recipe_Ingredient ri ON r.id = ri.recipe_id 
    LEFT JOIN Ingredient i ON ri.ingredient_id = i.id 
    WHERE (r.name ILIKE ?1 OR i.name ILIKE ?1 OR r.name ILIKE ?2 OR i.name ILIKE ?2 ) --example for two keyword search 

    SELECT DISTINCT r.id as recipe_id, r.name as recipe_name, i.name as ingredient_name 
    FROM Recipe r 
    LEFT JOIN Recipe_Ingredient ri ON r.id = ri.recipe_id 
    LEFT JOIN Ingredient i ON ri.ingredient_id = i.id -- no keywords given, search all
```
    ``r.name ILIKE ?1 OR i.name ILIKE ?1`` clauses are added for each keyword searched

### User can see each indicidual recipe and its ingredients
```sql 
    SELECT recipe.id AS recipe_id, recipe.name AS recipe_name, recipe.instructions AS recipe_instructions
    FROM recipe 
    WHERE recipe.id = ? --for recipe data

    SELECT Ingredient.id, Ingredient.name, amount, Ingredient.measurement_unit 
    FROM Ingredient 
    INNER JOIN Recipe_Ingredient ON Ingredient.id = Recipe_Ingredient.ingredient_id 
    AND Recipe_Ingredient.Recipe_id = ? -- ingredients for recipe
```
