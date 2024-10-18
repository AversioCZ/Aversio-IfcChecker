import sys
import os
import webbrowser
import IDSChecker
from IDSChecker.gui import CheckerGUI

import logging


LOGGING_LEVEL = logging.INFO

def setup_logging():
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    logging.info("Starting the GUI application...")

    # Initialize and start the GUI application
    app = CheckerGUI()  # Create an instance of the GUI class
    app.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main()