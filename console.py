#!/usr/bin/python3
"""
Creation of the console of the web application
"""


import json
import re
import shlex
import cmd
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
import models


class HBNBCommand(cmd.Cmd):
    """
    The console class
    """
    prompt = '(hbnb) '
    classes = {"BaseModel", "User", "State",
               "City", "Amenity", "Place", "Review"}

    def default(self, line):
        """
        Default section, all the command not built-in gonna be procces here
        Process all the command line as: ClassName.function, where function is:
            all()
            show()
            destroy()
            count()
        Exceptions:
            If the syntaxe is not know
        """
        functionDict = {"all": self.do_all,
                        "show": self.do_show,
                        "destroy": self.do_destroy,
                        "count": self.do_count,
                        "update": self.do_update
                        }
        patern = r"(.*)\.(.*)\((.*)\)"
        if re.search(patern, line):
            args = re.sub(patern, r"\2 \1 \3", line)
            args = shlex.split(args)
            if args[0] in functionDict:
                if args[0] == "update" and "{" in line and "}" in line:
                    self.update_in_dict(args[1], line)
                else:
                    functionDict[args[0]](' '.join(args[1:]))
        else:
            print(f"*** Unknown syntax: {line}")

    def emptyline(self):
        """
        The case of empty line
        """
        print(end="")

    def do_EOF(self, line):
        """
        Manage the EOF
        """
        return True

    def do_quit(self, line):
        """
        Quit the program
        """
        return True

    def do_count(self, line):
        """
        Count the number of given ClassName instance
        """
        args = shlex.split(line)
        count = 0
        for instance in models.storage.all().values():
            if instance.__class__.__name__ == args[0]:
                count += 1
        print(count)

    def do_create(self, className):
        """
        Create a new instance of the given class
        Usage: create <NameClass>
        Exceptions:
            If the name class do not exist
            If the name class isn't given
        """
        if not className:
            print("** class name missing **")
            return False
        data = shlex.split(className)
        try:
            newClass = eval(data[0])()
            print(newClass.id)
            newClass.save()
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """
        Show a instance by his ID and class name
        Usage: show <ClassName> <Id>
        Exceptions:
            If the name class is missing
            If the class do not exist
            Id is missing
            If the Id do not exist
        """
        if not line:
            print("** class name missing **")
            return False
        data = shlex.split(line)
        if data[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        if len(data) == 1:
            print("** instance id missing **")
            return False
        classNameId = f"{data[0]}.{data[1]}"
        if classNameId not in models.storage.all():
            print("** no instance found **")
            return False
        print(models.storage.all()[classNameId])

    def do_destroy(self, line):
        """
        Destroy a instance by his ID and class name
        Usage: destroy <ClassName> <Id>
        Exceptions:
            If the name class is missing
            If the class do not exist
            Id is missing
            If the Id do not exist
        """
        if not line:
            print("** class name missing **")
            return False
        data = shlex.split(line)
        if data[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        if len(data) == 1:
            print("** instance id missing **")
            return False
        classNameId = f"{data[0]}.{data[1]}"
        if classNameId not in models.storage.all():
            print("** no instance found **")
            return False
        del models.storage.all()[classNameId]
        models.storage.save()

    def do_all(self, line):
        """
        Display all instance of a class
        Usage: all <className>
        Exceptions:
            If the class do not exist
        """
        instanceListStr = []
        if not line:
            for instance in models.storage.all().values():
                instanceListStr.append(instance.__str__())
        else:
            if line not in self.classes:
                print("** class doesn't exist **")
                return False
            for instance in models.storage.all().values():
                if instance.__class__.__name__ == line:
                    instanceListStr.append(instance.__str__())
        print(instanceListStr)

    def update_in_dict(self, classname, line):
        """
        Convert argument passes in command in dictionnary
        for the command update and call the function do_update with all key
        """
        dictRepr = re.findall("({.*})", line)
        dictRepr[0] = dictRepr[0].replace('\'', "\"")
        args = json.loads(dictRepr[0])
        line_catch = re.findall("(\".*?\")", line)
        id_line = line_catch[0].replace("\"", "")
        for key, val in args.items():
            self.do_update(
                classname + " " + id_line + " " + key + " " + str(val)
            )

    def is_float(self, num):
        """
        Check if the string is a number
        """
        try:
            float(num)
            return True
        except ValueError:
            return False

    def do_update(self, line):
        """
        Update an attribute of an instance.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        Exceptions:
            If the name class is missing
            If the class do not exist
            Id is missing
            If the Id do not exist
            If no instance found
            If the attribute is missing
            If the value is missing
        """
        if not line:
            print("** class name missing **")
            return False
        line = line.replace(",", "")
        data = shlex.split(line)
        if data[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        if len(data) == 1:
            print("** instance id missing **")
            return False
        strLine = f"{data[0]}.{data[1]}"
        if strLine not in models.storage.all():
            print("** no instance found **")
            return False
        if len(data) == 2:
            print("** attribute name missing **")
            return False
        if len(data) == 3:
            print("** value missing **")
            return False
        currentInstance = models.storage.all()[strLine]
        if data[2] == "id" or data[2] == "created_at" or\
                data[2] == "updated_at":
            return False
        if data[3].isnumeric():
            data[3] = int(data[3])
        elif self.is_float(data[3]):
            data[3] = float(data[3])
        setattr(currentInstance, data[2], data[3])
        models.storage.save()

    def help_EOF(self):
        """
        Help section of EOF
        """
        print('Manage the EOF, exit the console and\
save all the created instance\n')

    def help_quit(self):
        """
        Help section of quit
        """
        print(
            'Quit function\n\
Usage quit\n\
Exit the console and save all the created instance\n')

    def help_create(self):
        """
        Help section of create
        """
        print(
            'Create function\n\
Usage create <ClassName>\n\
Create a new instance of the given class, print its id\n')

    def help_show(self):
        """
        Help section of show
        """
        print(
            'Show a instance by using the Nameclass and its ID\n\
Usage: show <ClassName> <Id>\n\
Show the __str__ representation of the class\n')

    def help_destroy(self):
        """
        Help section of destroy
        """
        print(
            'Destroy a instance by using the Nameclass and its ID\n\
Usage: destroy <ClassName> <Id>\n\
Destroy the instance, and save it into the Json file\n'
        )

    def help_all(self):
        """
        Help section of all
        """
        print("Display all instance of a class\n\
Usage: all <className>\n\
        "
              )

    def help_update(self):
        """
        Help section of update
        """
        print(
            'Update an attribute of an instance.\n\
Usage: update <class name> <id> <attribute name> "<attribute value>"\n'
        )

    def help_count(self):
        """
        Help section of count
        """
        print('Count the number of given ClassName instance\n\
Usage : count <class name>')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
