Setting up to use the database:

0. Import necessary modules for SQLAlchemy

    ```python
    from sqlalchemy import select
    import dependencies.database as db
    from dependencies.database import *
    ```

1. Initialize SQL session

    ```python
    db:Session = st.session_state["db_session"]
    ```

2. How to add to database

    ```python

    user = User( # Create instance of Object to be added
        username= "input",
        email= "some",
        password= "data",
        last_name= "in",
        first_name= "thes",
        middle_name= "fields",
        contact= "xdd",
        address= "",
        barangay= "",
        city= "",
        zipcode= "",
    )

    db.add(User) # Add to database
    db.commit() # Commit changes

    ```

3. How to select from database

    ```python
    # Create SQL expression (equivalent to SELECT * from customers)
    select_all_users = select(User) 
    
    # (equivalent to SELECT id, first_name from customers)
    select_id_name = select(User.id, User.first_name)

    # (equivalent to SELECT * from customers WHERE first_name = 'Gab'"
    select_gab = select(User).filter_by(first_name="Gab")
    # filter_by() filters by specific parameters


    # db.execute Executes SQL expression and returns a tuple
    
    # Returns string representation of all users
    for u in db.execute(select_all_users): 
        print(u) # Prints every user  

    # Returns only id and name of all users
    for i, n in db.execute(select_id_name):
        print(i, n) Prints: <User.id> <User.first_name>

    for n in db.execute(select_gab): 
        print(n) # Prints every user with first name Gab  