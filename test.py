from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDesktopWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Get the screen size and set the window size
        screen = QDesktopWidget().screenGeometry()  
        self.setGeometry(0, 0, screen.width(), screen.height())  

        # Create a label
        self.label = QLabel("PyQt5 is working!", self)
        self.label.move(0, 0) 

        self.center_label()

    def center_label(self):
        # Get the screen size
        screen = QDesktopWidget()
        screen_geometry = screen.screenGeometry()

        # Get window size
        window_geometry = self.geometry()

        # Calculate the center position for the label
        label_x = (window_geometry.width() - self.label.width()) // 2
        label_y = (window_geometry.height() - self.label.height()) // 2

        # Move the label to the calculated position
        self.label.move(label_x, label_y)


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
