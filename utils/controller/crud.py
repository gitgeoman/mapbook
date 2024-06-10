def read_user(users: list) -> None:
    print("About your friends: ")
    for user in users:
        print(f'\tYour friend {user["name"]} {user["surname"]} sends {user["posts"]} posts.')


def add_user(lista: list) -> None:
    new_user: dict = {
        "name": input("Type  new user name: "),
        "surname": input("Type new user surname: "),
        "posts": int(input("Type how many post did new user published: ")),
        'location': input("Type new user location: ")
    }
    lista.append(new_user)


def search_user(users: list) -> dict:
    name: str = input("Who do you look for (name): ")
    for user in users:
        if user["name"] == name:
            return user


def remove_user(users: list) -> None:
    name: str = input("Type a name of user to be removed: ")
    for user in users:
        if user["name"] == name:
            users.remove(user)


def update_user(users: list) -> None:
    name: str = input("Type a name of user you like to update: ")
    for user in users:
        if user["name"] == name:
            user["name"] = input("Type new name: ")
            user["surname"] = input("Type new surname: ")
            user["posts"] = int(input("Type new number of posts: "))
