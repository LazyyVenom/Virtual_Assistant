# Sasta Tony Stark - Gesture Controller

A gesture-based controller using OpenCV, Mediapipe, numpy, and PyCaw libraries to control various system features such as volume, brightness, window management, and a game controller using hand gestures captured via a webcam. This project also includes a gesture-based menu and a basic face filter to provide a Tony Stark-like experience.

## Features

1. **Gesture Controller**: Control multiple system features using different hand gestures.
2. **Game Remote**: Use hand gestures to control game functionalities.
3. **Volume Control**: Adjust the system volume with specific hand gestures.
4. **Brightness Control**: Adjust the system brightness with specific hand gestures.
5. **Exit**: Exit the application using a specific hand gesture held for 2 seconds.

## Gesture Mappings

- **1 Finger**: Activate Gesture Controller.
- **2 Fingers**: Activate Game Remote.
- **3 Fingers**: Control Volume.
- **4 Fingers**: Control Brightness.
- **5 Fingers (hold for 2 seconds)**: Exit the Application.

## Demo Images

| Gesture | Function            | Image                                        |
|---------|---------------------|----------------------------------------------|
| 1 Finger| Gesture Controller  | ![Gesture Controller](./demo/gesture1.png)   |
| 2 Fingers| Game Remote       | ![Game Remote](./demo/gesture2.png)          |
| 3 Fingers| Volume Control    | ![Volume Control](./demo/gesture3.png)       |
| 4 Fingers| Brightness Control| ![Brightness Control](./demo/gesture4.png)   |
| 5 Fingers| Exit              | ![Exit](./demo/gesture5.png)                 |

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/LazyyVenom/Virtual_Assistant.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Virtual_Assistant
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main script:
    ```bash
    python VirtualAssistant.py
    ```
2. Use the predefined hand gestures to control the features.

## Libraries Used

- OpenCV
- Mediapipe
- PyAutoGUI
- screen_brightness_control
- numpy
- PyCaw

## Contribution

Feel free to fork this repository and contribute by submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact choubey.anubhav253@gmail.com.
