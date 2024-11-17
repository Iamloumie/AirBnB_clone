#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        # Initialize line elements
        _cmd = _cls = _id = _args = ''

        # Scan for general formatting - i.e. '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            # Parse line left to right
            pline = line[:]
            
            # Isolate <class name>
            _cls = pline[:pline.find('.')]

            # Isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # If parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # Partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # Isolate _id, stripping quotes
                _id = pline[0].replace('"', '')

                # If arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # Check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')

            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass

        return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[args]()
        storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ <class name>.show(<id>) """
        if '.' in args:
            class_name, object_id = args.split('.')
        else:
            class_name, object_id = args.split(' ')
        key = f"{class_name}.{object_id}"
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif key not in storage._FileStorage__objects:
            print("** no instance found **")
        else:
            print(storage._FileStorage__objects[key])

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: <className>.show(<objectId>)\n")

    def do_destroy(self, args):
        """ <class name>.destroy(<id>) """
        if '.' in args:
            class_name, object_id = args.split('.')
        else:
            class_name, object_id = args.split(' ')
        key = f"{class_name}.{object_id}"
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif key not in storage._FileStorage__objects:
            print("** no instance found **")
        else:
            del storage._FileStorage__objects[key]
            storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: <className>.destroy(<objectId>)\n")

    def do_all(self, args):
        """ <class name>.all() """
        print_list = []
        for key, obj in storage._FileStorage__objects.items():
            class_name = key.split('.')[0]
            if not args or class_name == args:
                print_list.append(str(obj))
        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: <className>.all()\n")

    def do_count(self, args):
        """ <class name>.count() """
        count = 0
        for key in storage._FileStorage__objects:
            if args == key.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: <class_name>.count()")

    def do_update(self, args):
        """ Updates a certain object with new info """
        parts = args.split()
        if len(parts) < 2:
            print("** class name missing **")
            return
        class_name = parts[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(parts) < 3:
            print("** instance id missing **")
            return
        object_id = parts[1]

        key = f"{class_name}.{object_id}"
        if key not in storage._FileStorage__objects:
            print("** no instance found **")
            return

        obj = storage._FileStorage__objects[key]
        if len(parts) == 3 and '{' in parts[2] and '}' in parts[2]:
            kwargs = eval(parts[2])
            for k, v in kwargs.items():
                if k in HBNBCommand.types:
                    v = HBNBCommand.types[k](v)
                    setattr(obj, k, v)
                else:
                    if len(parts) < 4:
                        print("** attribute name missing **")
                        return
                    attribute_name = parts[2]
                    if len(parts) < 5:
                        print("** value missing **")
                        return
                    attribute_value = ' '.join(parts[3:])
                    if attribute_name in HBNBCommand.types:
                        attribute_value = HBNBCommand.types[attribute_name](attribute_value)
                        setattr(obj, attribute_name, attribute_value)
            obj.save()


    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: <className>.update(<id> <attName> <attVal>)\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
