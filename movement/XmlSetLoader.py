import xml.etree.ElementTree as ElemTree

from movement.MovementError import MovementError
from movement.SetOfMovements import SetOfMovements
from movement.Movement import Movement


class XmlSetLoader:

    def __init__(self, path):
        self.path = path

    def load_xml_set(self):
        # Create object that encapsulates the set.
        set_of_movements = SetOfMovements()

        # Get root of xml file.
        root_xml = ElemTree.parse(self.path).getroot()

        # Get information about the set
        set_of_movements.name = root_xml.find('name').text
        set_of_movements.description = root_xml.find('description').text

        # Get each movement for this set.
        for mov_xml in root_xml.findall('movement'):
            # Create object that encapsulates the movement.
            movement = Movement()

            # Get information about the movement.
            movement.name = mov_xml.find('movement-name').text
            movement.description = mov_xml.find('movement-description').text
            movement.feedback_message = mov_xml.find('movement-feedback-message').text

            # Get template of this movement
            movement.template = mov_xml.find('movement-template').text

            # Get root of errors for this movement.
            err_root_xml = mov_xml.find("errors")
            # Get each error for this movement.
            for mov_err_xml in err_root_xml.findall('movement-error'):
                # Create object that encapsulates the movement errors.
                movement_error = MovementError()

                # Get information about the movement error.
                movement_error.name = mov_err_xml.find('movement-error-name').text
                movement_error.description = mov_err_xml.find('movement-error-description').text
                movement_error.feedback_message = mov_err_xml.find('movement-error-feedback-message').text

                # Get template of this movement
                movement_error.template = mov_err_xml.find('movement-error-template').text

                # Add this error to the movement.
                movement.movement_errors.append(movement_error)

            # Append the movement to the st
            set_of_movements.movements.append(movement)

        # Return loaded set.
        return set_of_movements
