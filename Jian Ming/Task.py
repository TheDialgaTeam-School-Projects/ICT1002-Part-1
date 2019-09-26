import threading


class Task(threading.Thread):
    """
    Class that handles background task that can return the result after the execution.
    """

    def __init__(self, callback, output=None, *args, **kwargs):
        """
        Create a task that can return values in a queue.

        :param function callback: Function to run in the thread. Function must have the following parameter: def task(output, *args, **kwargs)
        :param Queue.Queue output: Queue that will return after the task ends.
        :param args: Array of args to pass into the callback function.
        :param kwargs: Dictionary of args to pass into the callback function.
        :rtype: Task
        :return: Task that would return by a given queue reference.
        """
        threading.Thread.__init__(self)

        self.callback = callback
        self.output = output
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Start the task in a new thread.
        """
        if self.output is not None:
            self.callback(self.output, *self.args, **self.kwargs)
        else:
            self.callback(*self.args, **self.kwargs)
