def read_user(users: list) -> None:
    """
    Displays information about the user's friends based on a list of dictionaries containing data about these friends.

    :param users: A list of dictionaries, where each dictionary represents a friend and contains the following keys:
        - "name" (str): The friend's first name.
        - "surname" (str): The friend's last name.
        - "posts" (int): The number of posts published by the friend.
    :return: None: This function does not return any value.

    Functionality:
    1. The function displays the header: "Information about your friends:".
    2. It iterates over each dictionary in the `users` list.
    3. For each friend, it displays their first name, last name, and the number of posts published in the formatted form:
       "Your friend {name} {surname} has published {posts} posts."

    Example usage:
    users_data = [
        {"name": "John", "surname": "Doe", "posts": 5},
        {"name": "Anna", "surname": "Smith", "posts": 12},
        {"name": "Peter", "surname": "Brown", "posts": 7}
    ]

    read_user(users_data)

    Output:
    Information about your friends:
        Your friend John Doe has published 5 posts.
        Your friend Anna Smith has published 12 posts.
        Your friend Peter Brown has published 7 posts.

    Notes:
    - The function assumes that each dictionary in the `users` list contains the keys "name", "surname", and "posts".
    - There is no error handling for cases where a dictionary is missing the required keys or has incorrect data types.
    """
    print("About your friends: ")
    for user in users:
        print(f'\tYour friend {user["name"]} {user["surname"]} sends {user["posts"]} posts.')


def add_user(lista: list) -> None:
    """
    Adds a new user to the provided list of users.

    :param lista: A list of dictionaries, where each dictionary represents a user.
    :return: None: This function does not return any value.

    Functionality:
    1. Prompts the user to input the name, surname, number of posts, and location of the new user.
    2. Creates a new dictionary with these values.
    3. Appends the new dictionary to the provided list.

    Example usage:
    users_list = []
    add_user(users_list)

    Expected input sequence:
    Type new user name: John
    Type new user surname: Doe
    Type how many posts did new user publish: 5
    Type new user location: New York

    Result:
    The users_list will contain one dictionary with the user's information.

    Notes:
    - The function assumes that the input values are correctly formatted.
    - There is no error handling for invalid inputs.
    """
    new_user: dict = {
        "name": input("Type  new user name: "),
        "surname": input("Type new user surname: "),
        "posts": int(input("Type how many post did new user published: ")),
        'location': input("Type new user location: ")
    }
    lista.append(new_user)


def search_user(users: list) -> dict:
    """
       Searches for a user by name in the provided list of users and returns the user's dictionary if found.

       :param users: A list of dictionaries, where each dictionary represents a user.
       :return: dict: The dictionary of the user found, or None if no user is found.

       Functionality:
       1. Prompts the user to input the name of the user they are searching for.
       2. Iterates over the list of users to find a match by name.
       3. Returns the dictionary of the first matching user found.

       Example usage:
       users_list = [
           {"name": "John", "surname": "Doe", "posts": 5, "location": "New York"},
           {"name": "Anna", "surname": "Smith", "posts": 12, "location": "London"}
       ]
       result = search_user(users_list)

       Expected input sequence:
       Who do you look for (name): John

       Result:
       The function returns the dictionary: {"name": "John", "surname": "Doe", "posts": 5, "location": "New York"}

       Notes:
       - The function assumes that names are unique within the list.
       - There is no error handling for cases where no user is found.
       """
    name: str = input("Who do you look for (name): ")
    for user in users:
        if user["name"] == name:
            print(user)
            return user


def remove_user(users: list) -> None:
    """
       Removes a user by name from the provided list of users.

       :param users: A list of dictionaries, where each dictionary represents a user.
       :return: None: This function does not return any value.

       Functionality:
       1. Prompts the user to input the name of the user to be removed.
       2. Iterates over the list of users to find a match by name.
       3. Removes the first matching user found from the list.

       Example usage:
       users_list = [
           {"name": "John", "surname": "Doe", "posts": 5, "location": "New York"},
           {"name": "Anna", "surname": "Smith", "posts": 12, "location": "London"}
       ]
       remove_user(users_list)

       Expected input sequence:
       Type a name of user to be removed: John

       Result:
       The users_list will no longer contain the dictionary with {"name": "John", "surname": "Doe", "posts": 5, "location": "New York"}.

       Notes:
       - The function assumes that names are unique within the list.
       - There is no error handling for cases where no user is found.
       """
    name: str = input("Type a name of user to be removed: ")
    for user in users:
        if user["name"] == name:
            users.remove(user)


def update_user(users: list) -> None:
    """
        Updates the information of an existing user in the provided list of users.

        :param users: A list of dictionaries, where each dictionary represents a user.
        :return: None: This function does not return any value.

        Functionality:
        1. Prompts the user to input the name of the user to be updated.
        2. Iterates over the list of users to find a match by name.
        3. Prompts the user to input new values for the user's name, surname, and number of posts.
        4. Updates the user's dictionary with the new values.

        Example usage:
        users_list = [
            {"name": "John", "surname": "Doe", "posts": 5, "location": "New York"},
            {"name": "Anna", "surname": "Smith", "posts": 12, "location": "London"}
        ]
        update_user(users_list)

        Expected input sequence:
        Type a name of user you like to update: John
        Type new name: Jonathan
        Type new surname: Doe-Smith
        Type new number of posts: 10

        Result:
        The dictionary with {"name": "John", "surname": "Doe", "posts": 5, "location": "New York"} will be updated to
        {"name": "Jonathan", "surname": "Doe-Smith", "posts": 10, "location": "New York"}.

        Notes:
        - The function assumes that names are unique within the list.
        - There is no error handling for cases where no user is found or for invalid inputs.
        """
    name: str = input("Type a name of user you like to update: ")
    for user in users:
        if user["name"] == name:
            user["name"] = input("Type new name: ")
            user["surname"] = input("Type new surname: ")
            user["posts"] = int(input("Type new number of posts: "))
