#!/usr/bin/python3

"""
program that contains the entry point of the command interpreter
"""

import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class HBNBCommand(cmd.Cmd):
    """
    The class of the command interpreter
    """

    prompt = "(iamloumie@hbnb)  "
    valid_classes = ["BaseModel", "User", "Amenity",
                     "City", "Place", "Review", "State"]

    def emptyline(self):
        """
        Do Nothing when an empty line is entered
        """
        pass

    def do_quit(self, arg):
        """
        exit the program
        """
        return True

    def help_quit(self, arg):
        """
        what to display when help is clicked
        """
        print("Quit command to exit the program")

    def do_EOF(self, arg):
        """
        what happens when you press ctrl + D
        """
        print()
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing**")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist**")
        else:
            new_instance = eval(f"{commands[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)  # Usage: Classname ID

        if len(commands) == 0:
            print("** class name missing**")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist**")
        elif len(commands) < 2:
            print("** instance id missing**")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** No instance found**")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing**")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist**")
        elif len(commands) < 2:
            print("** instance id missing**")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        print string representation of all instances or a specific class
        Usage: all [class_name]
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split(".")[0] == commands[0]:
                    print(str(value))

    def default(self, arg):
        """
        Default behaviour for cmd module for invalid syntax
        """

        arg_list = arg.split(".")  # User.all() output: ['User', 'all()']
        print(f"{arg_list=}")

        # arg_list[0] = 'User'
        # arg_list[1] = 'all()' or arg_list = 'ID' in terms of do update
        incoming_class_name = arg_list[0]
        print(f"{incoming_class_name=}")

        command = arg_list[1].split("(")
        # command[0] = 'all()'    #command[0] = 'show' or update
        # command [1] = ')'       # command[1] = '"12w-241")'

        incoming_method = command[0]
        print(f"{incoming_method=}")

        # TASK 15 advanced

        # after splitting [0] - ['"123-241"', '']
        incoming_xtra_arg = command[1].split(")")[0]

        all_args = incoming_xtra_arg.split(",")
        # all_args[0] = id
        # all_args[1] = attribute_name
        # all_args[2] = attribute_value

        method_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.do_count,
        }

        # compare the incoming_methods with the keys of the dictionary
        if incoming_method in method_dict.keys():
            if incoming_method != "update":
                return method_dict[incoming_method](
                    "{} {}".format(incoming_class_name, incoming_xtra_arg)
                )
            else:
                obj_id = all_args[0]
                attribute_name = all_args[1]
                attribute_value = all_args[2]
                return method_dict[incoming_method](
                    "{} {} {} {}".format(
                        incoming_class_name, obj_id, attribute_name, attribute_value
                    )
                )

            # all User or show User 123

            # 'all User'
            # self.all(self, 'User')

        print("** Unknown syntax: {}".format(arg))
        return False

    def do_count(self, arg):
        """
        Counts and retrievs the number of instances of a class
        Usage: <class name>.count()
        """

        objects = storage.all()

        # User.count() City.count()
        # count User or count City

        commands = shlex.split(arg)  # after splitting, only class name is seen

        # commands[0] = 'class name'
        if arg:
            incoming_class_name = commands[0]

        count = 0

        if commands:
            if incoming_class_name in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == incoming_class_name:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating all attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value"
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]

                attr_name = commands[2]
                attr_value = commands[3]

                try:
                    attr_value = eval(attr_value)
                except Exception:
                    pass
                setattr(obj, attr_name, attr_value)

                obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
