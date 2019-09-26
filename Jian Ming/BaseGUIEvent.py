class BaseGUIEvent:
    def __init__(self, controller):
        """
        Handle event for GUI.

        :param MainGUI.MainGUI controller: Controller to access other GUI screens.
        :rtype: BaseGUIEvent
        :return: Event for GUI.
        """
        self.controller = controller

    def load(self, *args, **kwargs):
        """
        GUI onload event. All GUI data model should be load here.

        :param args: Array of args that was pass from the previous frame.
        :param kwargs: Dictionary of args that was pass from the previous frame.
        """
        pass
