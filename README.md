# Time Tracker Application

I have developed this time tracking tool to help me manage my time more effectively. It is written in Python and uses the PyQt library for its graphical user interface.

## Features

- **Time Logging:** The application allows users to log the time they have worked. The time can be entered in seconds (s), minutes (m), or hours (h). If the time entered is more than 24 hours, it will be capped at 24 hours.

- **Table View:** The logged time is displayed in a table view. Each row in the table represents a different day, and the time worked on that day is displayed in the second column.

- **Data Persistence:** The application saves the logged time data using JSON, allowing users to close the application and return to it later without losing their data.

- **Time Editing:** Users can edit the time they have previously logged. If the time for the current day is edited, the timer display is also updated.

- **Graph View:** The application includes a graph view that visualizes the worked hours over time. The graph displays the total hours worked for each day, allowing users to easily track their progress and identify patterns.


## Usage

To use the application, simply run `app.py`. The application will open a window where you can log and view your time. To log time, enter the time worked in the appropriate format (e.g., "2h" for 2 hours) in the second column of the table. The application will automatically save your data.

## Code Structure

The code is structured around a main `MainWindow` class, which handles the application logic. The `cell_changed` method, for example, is triggered when a cell in the table is edited. It updates the time worked based on the new input and saves the data.

## Future Improvements

Future improvements to the application could include:

- Adding the ability to track time across multiple projects.
- Improving the user interface for a more intuitive user experience.
