class MenuCommand:
    def __init__(self, value, var, callback):
        """
        Set menu command to receive a value in a callback.

        :param str value: The value of the selected menu.
        :param Tkinter.StringVar var: The variable that contains the selected menu.
        :param function callback: The function to invoke when this menu is selected. Function must have the following parameter: def task(selected_item)
        :rtype: MenuCommand
        :return: Menu command to receive a value in a callback.
        """
        self.value = value
        self.var = var
        self.callback = callback

    def __call__(self, *args, **kwargs):
        """
        Invoke this function when this menu is selected.

        :param args: Array of args pass from the menu command.
        :param kwargs: Dictionary of args pass from the menu command.
        """
        if self.var is not None:
            self.var.set(self.value)

        if self.callback is not None:
            self.callback(self.value)
