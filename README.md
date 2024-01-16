# Logcat-Tools

The Logcat Tools is a Python-based graphical user interface (GUI) application designed to streamline the process of monitoring and analyzing Android device logs using the Android Debug Bridge (ADB). This tool provides a user-friendly interface to interact with ADB commands and view real-time logcat output from connected Android devices.

Features:

Start Logcat: Initiates the ADB logcat command to display real-time logs from the connected Android device.

Start Logcat with Grep: Enables filtering logcat output based on a specified grep command entered by the user.

Reboot Device: Triggers a device reboot using the ADB reboot command.

Clear Logcat: Clears the current logcat display and removes existing logcat logs from the connected device.

Set Logcat to Verbose: Sets the device logcat to verbose mode, providing more detailed logging information.

Set Logcat Size: Allows the user to set the maximum size of logcat logs by specifying the size in megabytes.

Change Theme: Toggles between black and white themes for better visibility.

Stop: Stops the ongoing logcat operation.

Stop and Save Logs: Stops logcat and saves the displayed logs to a timestamped log file.

Close: Exits the application.

Usage:

Ensure that Python and ADB are installed on the system.
Connect an Android device to the computer via USB and enable USB debugging.
Run the ADB Logcat Viewer program.
Use the provided buttons to perform various ADB logcat operations.
View and analyze real-time logs in the GUI.
Save logs to files for future reference.
Note: The program checks for dependencies, updates them, and provides an intuitive interface for managing ADB logcat operations. It is suitable for developers, testers, and anyone interested in monitoring Android device logs efficiently.

Step 1: Prerequisites

Ensure that Python is installed on your computer. You can download it from python.org.
Install the Android Debug Bridge (ADB) on your computer. ADB is usually included in the Android Studio package, or you can download it separately from the official Android Developer website.

Step 2: Connect Android Device

Connect your Android device to your computer using a USB cable.
Enable USB debugging on your Android device. You can do this in the Developer Options section, which you can activate by tapping the "Build number" in the device's Settings multiple times.

Step 3: Run the Logcat Tools

Download and extract the Logcat Tools Python script.
Open a terminal or command prompt in the directory where the script is located.
Step 4: Install Dependencies

Run the script by executing the command: python logcattools.py. This will check for dependencies (Python and ADB) and prompt you to install or upgrade them if needed.

Step 5: Launch the Logcat Tools

After installing/upgrading dependencies, the Logcat tools GUI will open.
You will see a set of buttons on the left side and a log display on the right side.

Step 6: Start Logcat

Click the "Start Logcat" button to initiate the ADB logcat command. This will display real-time logs from your connected Android device in the log display area.
Step 7: Start Logcat with Grep (Optional)

If you want to filter logs based on a specific keyword, enter the keyword in the entry field provided.
Click the "Start Logcat with Grep" button to apply the grep command.

Step 8: Perform Additional Operations (Optional)

Use other buttons to perform operations such as rebooting the device, clearing logcat, setting logcat to verbose mode, setting logcat size, changing the theme, stopping logcat, or stopping and saving logs.

Step 9: Save Logs (Optional)

If you want to save the displayed logs to a file, click the "Stop and Save Logs" button. The logs will be saved in a file with a timestamped filename.

Step 10: Close the Logcat Tools

Click the "Close" button to exit the application.
Note: The Logcat Tools provides an interactive and convenient way to manage ADB logcat operations, making it useful for developers, testers, and anyone interested in monitoring Android device logs efficiently.


