# How to use the program
For general definition of the program see [readme](https://github.com/jjjjm/Tsoha-RecipeDatabase/blob/master/README.md) and [User cases](https://github.com/jjjjm/Tsoha-RecipeDatabase/blob/master/documentation/use-cases-and-sql.md)

## Account creation and logging in
You can create an account by clicking the **Create new account** button or by navigating to ``/login/new/`` paga, and filling out the form. 
Minimum length for username: 2 and for password: 6. Your username also has to be unique, i.e. not already present in the db.  
After a succesful account creation you should be redirected to login screen where you can insert your credientials to login.
(**Login** from menu-bar, or navigate to ``/login/`` page)

## Basic functionality
### While not logged in
``/recipes/`` page (**Recipes** from menu bar):
You can search recipes by inserting keywords for recipe names and ingredient, separeted by comma and pressing the search button.
For example, if insert ``coffee, milk`` as keywords, and the db has recipes named ``Coffee Cake`` and ``Porridge``(which has ingredient ``milk``),
the search will yield both ``Coffee Cake`` and ``Porridge``.

### While logged in
``/ingredients/`` page (**Your ingredients** from menu bar):
You can create new ingredient with the form labeled **Add new ingredient** and give it an amount you currently have.
You can also edit the amounts of your ingredients, or delete them from your inventory with the buttons next to each ingredient.

``/ingredients/all/`` page (**List all ingredients** from menu bar):
See all the ingredient currently in the database, even those you don't have in your inventory.
You can add them to your inventory with amount values, checkinh the checkbox in the rows you want to add and then pressing the **Add all selected ingredients** button. 
If you try to add ingredient you already have, the program will notify that this can't be done by an error message.

``/recipes/new/`` page (**Add recipe** from menu bar):
Here you can add a new recipe with the ingredients you currently have in your inventory. Name is mandatory, instructions and ingredient optional. Select as many ingredient you want by checking the checkboxes next to them and giving them the amount needed in the recipe. Instructions support white spaces and linebreaks as formatting options (instructions are rendered as you write them)

``/recipes/`` page (**Recipes** from menu bar):
Same as the not logged in. The site also displays all the recipes you can currently make (that is, you have the needed ingredients in your inventory and have atleast the amount needed for the recipe, for each ingredient)

### While logged in as admin
``/admin/`` page (**Admin page** from menu bar):
You can delete any ingredient,recipe or user. You can also change the admin status of users. (These apply for your current account aswell, so be careful as if all admin accounts are removed the only way to change that is through direct db connection)

## Security
- All passwords are hashed
- CSFR-token is in use for all database queires that insert permanent data or modify information.
- All parameters are passed with ``VALUES`` keyword to mitigate sql-injections 


## Missing implementations and problems
### Missing
- Associate a recipe with user and mark them as private etc.
- With no user-recipe relation, currently editing recipes is impossible aswell
- Add pictures to recipes
- Association similiarly named ingredients
- Multiple measurement unit to one ingredient relation
- Ability to "cook recipe", that is automatically reducing the amount of ingredient in inventory with recipe amounts 
### Problems
- CSRF-token can sometimes be temperemental on it's usage
- Layout can still break on some sites with too long values (Names, measurement units etc.)
- Unknown behavior of LIKE clause in postgres (ILIKE seemed to fix the problem to some extent)
- Keyword search implementation is really really stupid atm
