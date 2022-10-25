
class Movement:

    def __init__(self):
        # Information about this movement.
        self.name = ""
        self.description = ""
        self.feedback_message = ""
        # Start and ending frame.
        self.start_frame = 0
        self.end_frame = 0
        # List containing key_points used in this movement.
        self.key_points = []
        # List containing errors that can be committed while executing this movement.
        self.movement_errors = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_feedback_message(self):
        return self.feedback_message

    def set_feedback_message(self, feedback_message):
        self.feedback_message = feedback_message

    def get_start_frame(self):
        return self.start_frame

    def set_start_frame(self, start_frame):
        self.start_frame = start_frame

    def get_end_frame(self):
        return self.end_frame

    def set_end_frame(self, end_frame):
        self.end_frame = end_frame

    def add_keypoint(self, keypoint):
        self.key_points.append(keypoint)

    # noinspection DuplicatedCode
    def remove_keypoint(self, keypoint):
        index = 0
        found = False
        for i in range(len(self.key_points)):
            if keypoint == self.key_points[i].name:
                found = True
                index = i
                break
        if found:
            del self.key_points[index]

    def get_key_points(self):
        return self.key_points

    def get_keypoint(self, name):
        res_keypoint = None
        for keypoint in self.key_points:
            if name == keypoint.name:
                res_keypoint = keypoint
                break
        return res_keypoint

    def get_keypoint_names(self):
        names = []
        for keypoint in self.key_points:
            names.append(keypoint.name)
        return names

    def add_movement_error(self, movement):
        self.movement_errors.append(movement)

    # noinspection DuplicatedCode
    def remove_movement_error(self, name):
        index = 0
        found = False
        for i in range(len(self.movement_errors)):
            if name == self.movement_errors[i].name:
                found = True
                index = i
                break
        if found:
            del self.movement_errors[index]

    def get_movement_errors(self):
        return self.movement_errors

    def get_movement_error(self, name):
        res_movement = None
        for movement_error in self.movement_errors:
            if name == movement_error.name:
                res_movement = movement_error
                break
        return res_movement

    def get_movement_error_names(self):
        names = []
        for movement_error in self.movement_errors:
            names.append(movement_error.name)
        return names
