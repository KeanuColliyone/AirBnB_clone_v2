#!/usr/bin/python3
"""The command interpreter's entry point module."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand (cmd.Cmd):

    """The command interpreter's class"""

    prompt = "(hbnh) "

    def _precmd(self, line):
        """Intercepts commands to test for class.method() syntax."""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line

        classname, method, args = match.groups()
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)

        if match_uid_and_args:
            uid, attr_or_dict = match_uid_and_args.groups()
        else:
            uid, attr_or_dict = args, None

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            else:
                match_attr_and_value_regex = (
                    r'^(?:"([^"]*)")?(?:, (.*))?$'
                )
                match_attr_and_value = re.search(
                    match_attr_and_value_regex, attr_or_dict
                )
                if match_attr_and_value:
                    attr, value = match_attr_and_value.groups()
                    attr_and_value = (attr or "") + " " + (value or "")

        command = f"{method} {classname} {uid} {attr_and_value}".strip()
        self.onecmd(command)
        return ""

    def default(self, line):
        """When the command prefix is not recognized."""
        print(f"*** Unknown command: {line}")
        
    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')

        try:
            d = json.loads(s)
        except json.JSONDecodeError:
            print("** error: dictionary not valid JSON **")
            return

        if not classname:
            print("** class name missing **")
            return
        if classname not in storage.classes():
            print("** class doesn't exist **")
            return
        if not uid:
            print("** instance id missing **")
            return

        key = "{}.{}".format(classname, uid)
        if key not in storage.all():
            print("** no instance found **")
            return

        attributes = storage.attributes().get(classname, {})
        instance = storage.all()[key]
        for attribute, value in d.items():
            if attribute in attributes:
                try:
                    value = attributes[attribute](value)
                except (ValueError, TypeError):
                    print(f"** error: wrong type for {attribute} **")
                    continue
            setattr(instance, attribute, value)
        instance.save()

    def do_EOF(self, line):
        """Handles End Of File character."""
        print()
        return True

    def do_quit(self, line):
        """Exits the program."""
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER."""
        pass

    def do_create(self, line):
        """Creates an instance."""
        if not line:
            print("** class name missing **")
            return
        try:
            if line not in storage.classes():
                print("** class doesn't exist **")
                return
            instance = storage.classes()[line]()
            instance.save()
            print(instance.id)
        except Exception as e:
            print(f"Error: {e}")

    def do_show(self, line):
        """Prints the string representation of an instance."""
        if not line:
            print("** class name missing **")
            return
        words = line.split(' ')
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(words) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(words[0], words[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        if not line:
            print("** class name missing **")
            return
        words = line.split(' ')
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(words) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(words[0], words[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances."""
        if line:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
                return
            obj_list = [str(obj) for key, obj in storage.all().items()
                        if type(obj).__name__ == words[0]]
        else:
            obj_list = [str(obj) for key, obj in storage.all().items()]
        print(obj_list)

    def do_count(self, line):
        """Counts the instances of a class."""
        if not line:
            print("** class name missing **")
            return
        if line not in storage.classes():
            print("** class doesn't exist **")
            return
        matches = [k for k in storage.all() if k.startswith(line + '.')]
        print(len(matches))

        def do_update(self, line):
            """Updates an instance by adding or updating attribute."""
            if not line:
                print("** class name missing **")
                return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        if not match:
            print("** class name missing **")
            return
        
        classname, uid, attribute, value = match.groups()

        if classname not in storage.classes():
            print("** class doesn't exist **")
        elif not uid:
            print("** instance id missing **")
        else:
            key = f"{classname}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                if not re.search('^".*"$', value):
                    try:
                        value = float(value) if '.' in value else int(value)
                    except ValueError:
                        pass
                else:
                    value = value.strip('"')

                attributes = storage.attributes().get(classname, {})
                if attribute in attributes:
                    value = attributes[attribute](value)
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
