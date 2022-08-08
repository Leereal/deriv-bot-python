import signal, threading, orders

class Bot:
    
    def __init__(self, stake: float, expiration: int):
        """Constructor of the bot. It justs fills the needed informartion for the bot.
        Args:
            stake (float): Lotage to be used by the bot.
            time_period (int): Time period of the bot, 1 minute, 15 minutes... (in seconds)
            market (str): Market to operate in.
        """
        self.threads = []
        self.data = {'symbol': '', 'trade_option': ''}
        self.pill2kill = threading.Event()
        self.trading_data = {}
        self.trading_data['stake'] = stake
        self.trading_data['expiration'] = expiration      

    def thread_signals(self):
        """Function to launch the data thread."""
        t = threading.Thread(target=signal.thread_signal, 
                             args=(self.pill2kill, self.data))
        self.threads.append(t)
        t.start()
        print('Thread - DATA. LAUNCHED')

    def thread_orders(self):
        """Function to launch the thread for sending orders."""
        t = threading.Thread(target=orders.thread_orders, 
                             args=(self.pill2kill, self.data, self.trading_data))
        self.threads.append(t)
        t.start()
        print('Thread - ORDERS. LAUNCHED')
    
    def kill_threads(self):
        """Function to kill all the loaded threads."""
        print('Threads - Stopping threads')
        self.pill2kill.set()
        for thread in self.threads:
            thread.join()
            
    def start(self):
        """Function to start all the threads"""
        self.thread_signals()
        self.thread_orders()
    
    def wait(self):
        """Function to make the thread wait."""
        # Input para detener a los hilos
        print('\nPress ENTER to stop the bot\n')
        input()
        self.kill_threads()       