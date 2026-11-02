class User:
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age

    def display_details(self):
        return {
            "User ID": self.user_id,
            "Name": self.name,
            "Age": self.age
        }