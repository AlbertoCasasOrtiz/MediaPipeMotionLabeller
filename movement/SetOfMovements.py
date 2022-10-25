
class SetOfMovements:

    def __init__(self):
        # Information about the set.
        self.name = ""
        self.description = ""
        # Template from video of this set.
        self.template = None
        # List of movements contained in this set.
        self.movements = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_template(self):
        return self.template

    def set_template(self, template):
        self.template = template

    def add_movement(self, movement):
        self.movements.append(movement)

    # noinspection DuplicatedCode
    def remove_movement(self, name):
        index = 0
        found = False
        for i in range(len(self.movements)):
            if name == self.movements[i].name:
                found = True
                index = i
                break
        if found:
            del self.movements[index]
            return True
        else:
            return False

    def remove_movement_error(self, name):
        for movement in self.movements:
            removed = movement.remove_movement_error(name)
            if removed:
                return True
        return False

    def get_movements(self):
        return self.movements

    def get_movement(self, name):
        res_movement = None
        for movement in self.movements:
            if name == movement.name:
                res_movement = movement
                break
        return res_movement

    def get_movement_names(self):
        names = []
        for movement in self.movements:
            names.append(movement.name)
        return names
