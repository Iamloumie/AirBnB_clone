# HBNB - The Console

## Project Description

This project is a command-line interface implementation of an AirBnB clone.
It implements a backend interface to manage program data with console commands.
The console provides a set of tools to manipulate project objects like User, State, City, Place, etc.

## Command Interpreter Description

The command interpreter allows users to interact with the objects of the project using various commands.
You can create, retrieve, update, and delete objects, as well as manage file storage.

### How to Start It

```bash
$ ./console.py
```

### How to Use It

The console supports the following commands:

- `create`: Create a new instance of a class
- `show`: Show the details of a specific instance
- `destroy`: Delete a specific instance
- `all`: Display all instances or all instances of a specific class
- `update`: Update attributes of an instance

### Examples

```bash
$ ./console.py
(hbnb) create User
246c227a-d5c1-403d-9bc7-6a47bb9f0f68
(hbnb) show User 246c227a-d5c1-403d-9bc7-6a47bb9f0f68
(hbnb) all User
(hbnb) update User 246c227a-d5c1-403d-9bc7-6a47bb9f0f68 first_name "Betty"
```

## Project Structure

```
.
├── console.py               # Command interpreter
├── file.json               # JSON database
├── models/                 # Project models
│   ├── amenity.py         # Amenity model
│   ├── base_model.py      # Base model
│   ├── city.py            # City model
│   ├── engine/            # Storage engine
│   │   └── file_storage.py
│   ├── place.py           # Place model
│   ├── review.py          # Review model
│   ├── state.py           # State model
│   └── user.py            # User model
└── tests/                 # Unit tests
    └── test_models/       # Model tests
        ├── test_amenity.py
        ├── test_base_model.py
        ├── test_city.py
        ├── test_console.py
        ├── test_place.py
        ├── test_review.py
        ├── test_state.py
        └── test_user.py
```

## Testing

To run the unit tests:

```bash
$ python3 -m unittest discover tests
```
