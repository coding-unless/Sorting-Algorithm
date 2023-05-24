import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QWidget, QErrorMessage, QSpacerItem, QSizePolicy, QScrollArea)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
import time

def bubble_sort(arr):
    # This is an optimized version of bubble sort that stops early if no swaps are made in a pass.
    n = len(arr)
    for i in range(n):
        # Flag to check if any swaps are made in this pass
        swapped = False
        for j in range(n-i-1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # If no swaps are made in this pass, then the array is already sorted
        if not swapped:
            break
    return arr

def selection_sort(arr):
    """
    This is an iterative version of selection sort.
    """
    n = len(arr)
    for i in range(n-1):
        # Find the minimum element in the unsorted part of the array
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the minimum element with the first element in the unsorted part of the array
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def sort_array(sort_type, arr):
    """
    Sorts the array using bubble or selection
    """
    start_time = time.time()
    if sort_type == 'bubble':
        output_arr = bubble_sort(arr)
    elif sort_type == 'selection':
        output_arr = selection_sort(arr)
    global time_elapsed
    time_elapsed = time.time() - start_time
    print(f"Time elapsed for sorting: {time_elapsed:.5f} seconds")

    # Determine the maximum number of elements to display per row
    max_elements_per_row = 10

    # Split the sorted array into multiple rows
    output_arr_rows = [output_arr[i:i+max_elements_per_row] for i in range(0, len(output_arr), max_elements_per_row)]

    # Join the rows into a string with newline characters
    output_str = '\n'.join([str(row) for row in output_arr_rows])

    return output_str

class SortApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Sorting")
        self.setGeometry(100, 100, 600, 200)

        self.initUI()

    def initUI(self):
        # Set layout
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        output_layout = QHBoxLayout()

        # Set font
        font = QFont()
        font.setPointSize(12)

        # Input widgets
        self.label_input = QLabel("Enter an array (comma-separated):")
        self.label_input.setFont(font)
        self.entryinput = QLineEdit()
        self.entryinput.setFont(font)
        self.label_sort = QLabel("Sort type:")
        self.label_sort.setFont(font)
        self.combobox_sort = QComboBox()
        self.combobox_sort.addItems(['bubble', 'selection'])
        self.combobox_sort.setFont(font)
        self.button_sort = QPushButton("Sort")
        self.button_sort.setFont(font)

        # Set button color
        button_color = QColor(52, 152, 219)
        self.button_sort.setStyleSheet("background-color: %s; color: white;" % button_color.name())

        # Output widgets
        self.label_output = QLabel()
        self.label_output.setFont(font)

        # Set output label color
        output_color = QColor(46, 204, 113)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, output_color)
        self.label_output.setPalette(palette)

        # Add input widgets to layout
        input_layout.addWidget(self.label_input)
        input_layout.addWidget(self.entryinput)
        input_layout.addWidget(self.label_sort)
        input_layout.addWidget(self.combobox_sort)
        input_layout.addWidget(self.button_sort)

        # Add output widgets to layout
        output_layout.addWidget(self.label_output)

        # Add input and output layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)

        # Add spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Add scroll feature *pending
        scroll = QScrollArea() # 
        scroll.setWidgetResizable(True) #

        layout = QVBoxLayout(self) #
        layout.addWidget(scroll) #

        # Connect button to sort_array function
        self.button_sort.clicked.connect(self.sort_array)

    def sort_array(self):
        # Get the input array from the entry box
        input_str = self.entryinput.text()
        try:
            input_arr = [int(x.strip()) for x in input_str.split(',')]
        except ValueError:
            self.display_error("Invalid input: please enter integers separated by commas")
            return

        # Get the sort type from the combobox
        sort_type = self.combobox_sort.currentText()
        if not sort_type:
            self.display_error("Please select a sort type")
            return

        # Sort the array using the specified sort type
        output_arr = sort_array(sort_type, input_arr)

        # Display the sorted array in the output label
        self.label_output.setText(str(output_arr) + "\n" + str(time_elapsed) + "s")

    def display_error(self, message):
        """
        Displays an error message in a popup dialog.
        """
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sort_app = SortApp()
    icon_path ='./sort.svg'
    icon = QIcon(icon_path)
    sort_app.setWindowIcon(icon)        
    sort_app.show()
    sys.exit(app.exec_())
