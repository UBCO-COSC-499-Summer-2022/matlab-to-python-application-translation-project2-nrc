import threading
import traceback


class AsyncHandler:
    """
    A handler spins off another theread and returns immediately.
    Used with sliders and other GUI components to prevent laggy behaviour.
    """

    def __init__(self, handler):
        """Wraps a handler and returns an asynchronous handler."""
        self.handler = handler
        # there will be only one async thread being executed at any given time
        self.thread = None
        # indicates whether a call to handler is currently queued/delayed
        self.delay = False
        # these variables will store arguments in-case a call to the handler
        # must be delayed
        self.next_args = None
        self.next_kwargs = None
        # a lock that prevents any weird edge cases
        # the handler is the only thing not executed in it
        self.mutex = threading.Lock()

    def __call__(self, *args, **kwargs):
        """
        Calls the async handler which either spins off a thread,
        or delays the call if one is already running.
        """
        with self.mutex:
            if self.thread is None:
                self.thread = threading.Thread(
                    target=self.async_thread, args=args, kwargs=kwargs)
                self.thread.start()
            else:
                self.delay = True
                self.next_args = args
                self.next_kwargs = kwargs

    def async_thread(self, *args, **kwargs):
        """The main method to be run by the thread."""
        # this will loop until there are no more delayed calls to make
        while self.thread is not None:
            try:
                self.handler(*args, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                print(e)
            finally:
                with self.mutex:
                    if self.delay:
                        self.delay = False
                        args = self.next_args
                        kwargs = self.next_kwargs
                    else:
                        # no delayed calls, get out of here
                        self.thread = None
