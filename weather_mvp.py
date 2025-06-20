""" ********************************************
* Name - Rakesh  (i_mrakesh@outlook.com)       *
* Description -Weater Report data (MVP )       *
* Date: June 2025                              *
*******************************************  """

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit
from PySide6.QtCore import Signal, QObject

# MODEL - Reads file and segregates data into 8 sets
class Model(QObject):
    data_processed = Signal(dict)  # Signal to send structured data
    
    def load_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Example: Extract major sections (you can refine this logic)
        sections = {
            "Station Info": content.split("[Station Information]")[1].split("[Flight Start Time]")[0].strip(),
            "Flight Data": content.split("[Flight Start Time]")[1].split("[PTU summary]")[0].strip(),
            "PTU Summary": content.split("[PTU summary]")[1].split("[Highest Point]")[0].strip(),
            "Wind Data": content.split("[Wind Significant Levels]")[1].split("[Regional Wind Levels]")[0].strip(),
            "Cloud Data": content.split("[Cloud Data]")[1].split("[Standard Isobaric Surfaces]")[0].strip(),
            "Tropopause Data": content.split("[Tropopauses1]")[1].split("[Freezing Level]")[0].strip(),
            "Freezing Level": content.split("[Freezing Level]")[1].split("[Cloud Data]")[0].strip(),
            "Standard Isobaric Surfaces": content.split("[Standard Isobaric Surfaces]")[1].strip()
        }

        self.data_processed.emit(sections)  # Send processed data

# VIEW - UI with 8 tabs to display data
class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Data Viewer")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.text_areas = {name: QTextEdit() for name in [
            "Station Info", "Flight Data", "PTU Summary", "Wind Data",
            "Cloud Data", "Tropopause Data", "Freezing Level", "Standard Isobaric Surfaces"
        ]}
        
        for name, widget in self.text_areas.items():
            self.tabs.addTab(widget, name)

    def update_tabs(self, sections):
        for name, data in sections.items():
            self.text_areas[name].setText(data)  # Display segregated data

# PRESENTER - Connects Model signals to View slots
class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.data_processed.connect(self.view.update_tabs)  # Connect signal to slot

# RUN APPLICATION
app = QApplication([])
model = Model()
view = View()
presenter = Presenter(model, view)

view.show()
model.load_file("20240830-00-Integration_Data.txt")  # Load the attached file

app.exec()
