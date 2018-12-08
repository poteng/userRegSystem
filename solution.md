## generate_password()

* Complexity == 1: Return a password with only lowercase chars and **at least one lowercase char**
* Complexity == 2: Previous level plus at least 1 digit
* Complexity == 3: Previous levels plus at least 1 uppercase char
* Complexity == 4: Previous levels plus at least 1 punctuation char

My approach is to have appropriate character pool for each complexity, and randomly choose characters from it.

    lower = string.ascii_lowercase
    lower_number = string.ascii_lowercase + string.digits
    letters_number = string.ascii_letters + string.digits
    letters_number_punctuation = string.ascii_letters + string.digits + string.punctuation
 
To make sure all "at least one" conditions are met, I check every generated password and re-generate it if any condition is not met. Here is an example for complexity 2:

    elif complexity == 2:
        while not (any(c.isdigit() for c in password) and any(c.islower() for c in password)):
            password = ""
            for i in range(length):
                password += random.choice(lower_number)
I choose this approach for randomness purpose. There are other more efficient approaches but they might not have good randomness so I didn't choose them. (ex: generating needed characters first, then generating the rest of a password)

Also, deal with edge cases. 

Length:

    if length < complexity or length > 100:
        print('Length can\'t be negative or smaller than complexity or bigger than 100.')
        return ""
Complexity:

    else:
        print('Complexity can only be 1 ~ 4. Got ', complexity)
        
## check_password_level()

* Complexity 1: If a password has only lowercase chars and **at least one lowercase char**
* Complexity 2: Previous level condition and at least 1 digit
* Complexity 3: Previous levels condition and at least 1 uppercase char
* Complexity 4: Previous levels condition and at least 1 punctuation
* Complexity 1: **All other conditions**


* Complexity 2: password has length >= 8 chars and **is complexity 1**
* Complexity 3: password has length >= 8 chars and **is complexity 2**

Here I made a reasonable assumption again to define the condition more clearly.

My approach is to check if the password contain any lowercase/uppercase/digit/punctuation and if it's longer or equal than 8:

    contain_digit = any(c.isdigit() for c in password)
    contain_lower = any(c.islower() for c in password)
    contain_upper = any(c.isupper() for c in password)
    contain_punctuation = any(c in string.punctuation for c in password)
    longer_than_eight = len(password) >= 8
Then it's easy to check for complexity:

    if contain_lower and contain_upper and contain_digit and contain_punctuation:
        return 4
    elif contain_lower and contain_digit and (contain_upper or longer_than_eight):
        return 3
    elif contain_lower and (contain_digit or longer_than_eight):
        return 2
    elif contain_lower:
        return 1
    else:
        return 1
        
## Testing check_password_level()

I wrote a unit test script for testing. I used both manually generated passwords and randomly generated passwords to test. 

For manually generated test cases, all 4 complexities will be tested, with length longer than 8 or not. (8 test cases in total) 

    def test_check_password_level_with_level_1_long(self):
        password = 'aaafewer'
        self.assertEqual(check_password_level(password), 2, "Test failed: " + password)
        print("Success: check_password_level() with complexity 1 (long)")

For randomly generated test cases, because we have `generate_password()` function, we can use it as a support method to test. all 4 complexities will be tested 50 times each, with length longer than 8 or not. (400 tests in total)

    counter = 0
    for complex in range(1, 5):
        for i in range(50):
            counter += 1
            length = random.randrange(complex, 8)  # minimum length for a password is its complexty
            password = generate_password(length, complex)
            self.assertEqual(check_password_level(password), complex, "Test failed: " + password)
    print("Success: (random test) check_password_level() with complexity 1 ~ 4")
    print(counter, "random tests in total.")

I use manually generated passwords even though there is already a function `generate_password()` for generating passwords. The reason is that it's not a good approach to use randomly generated data to do unit test, because it sometimes causes problems when we want to replicate the same error.


## create_user()

I use *Requests* library to get a response object:

    url = 'https://randomuser.me/api/'
    r = requests.get(url)

Use *status_code* to check if the response is successful. Checking object itself or `r.json()` might not be useful, because the success of the call to r.json() does not indicate the success of the response. (According to http://docs.python-requests.org/)

    if r.status_code != requests.codes.ok:
        print('Failed response.')
        return - 1
Extract information from `r.json()`:

    data = r.json()
    first_name = data['results'][0]['name']['first']
    last_name = data['results'][0]['name']['last']
    full_name = first_name + ' ' + last_name
    email = data['results'][0]['email']

Store the information into the database:

    # the unique id will be assigned automatically by the database engine
    sql_insert_user = """INSERT INTO users(full_name,first_name,last_name,email)
                        VALUES(?,?,?,?)"""

    # create a connection to database
    conn = create_connection(db_path)
    create_user_table(conn)
    cursor = conn.cursor()
    cursor.execute(sql_insert_user, (full_name, first_name, last_name, email))
    conn.commit()

Where `create_connection()`, `create_user_table()`, `execute()` are the function I implemented to help with manipulating the database.

#### Some improvements
* In the database, I also created two additional columns for first name and full name, as it would benefit for future use.
* Made `create_user()` return the id of the row it inserted.

## Testing create_user()
Use `create_user()` to retrieve 10 users from the website, generate passwords for each user, and store them into the database for the corresponding user.

That's simple:

    name_db = 'user_login.db'
    conn = database_command.create_connection(name_db)
    
    for i in range(10):
        id_user = database_command.create_user(name_db)
        password = password.generate_password(random.randrange(6, 13), random.randrange(1, 5))
        database_command.update_password(conn, password, id_user)
    
    conn.close()

Use the row id returned by `create_user()` and use `update_password()` to update the password column with generated password. Repeat it 10 times.

The function `update_password()` simply update the password for a given raw id:

    sql_update_password = """ UPDATE users
                            SET password = ?
                            WHERE id = ? """
    cursor = conn.cursor()
    cursor.execute(sql_update_password, (password, id_user))
    conn.commit()
    