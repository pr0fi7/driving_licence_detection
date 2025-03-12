# Driving License Detection

The **Driving License Detection** project aims to simplify the work for parking services by detecting and extracting license plate numbers from video footages. Using advanced computer vision techniques like YOLO (You Only Look Once) for real-time object detection and OpenAIVision for enhanced image processing, this tool enables fast and accurate recognition of vehicle license plates, making parking management more efficient.

## Features

- **Real-time License Plate Detection**: Detect and extract license plate numbers from video footages using YOLO object detection.
- **OpenAIVision Integration**: Utilize OpenAIVision for enhanced image processing to improve accuracy.
- **Easy Integration**: The system can be integrated into parking services for automated vehicle tracking and monitoring.
- **High Efficiency**: Process videos quickly with high accuracy, reducing manual intervention in parking management.

## Installation

To get started with the Driving License Detection system, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/pr0fi7/driving_licence_detection.git
   cd driving_licence_detection

2. **Set Up the Virtual Environment**:

It's recommended to use a virtual environment to manage dependencies:

  ```bash
  python3 -m venv venv
  ```
3. Activate the Virtual Environment:

  - On Windows:
  ```bash
  venv\\Scripts\\activate
  ```
  - On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install Dependencies:

With the virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

5. Run the application
  To start the detection system, you can run the following command, where video_file.mp4 is your input video file containing the vehicle footages:
   ```bash
   python detect_license.py --input video_file.mp4 --output output_file.mp4
   ```
The system will process the video and extract the license plate numbers, saving the results to the specified output file.

6. ## Usage

The Driving License Detection system processes video footages and detects license plate numbers in real-time. You can customize the detection parameters and input/output formats according to your requirements.

## Contributing

Contributions to the Driving License Detection system are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Commit your changes with clear, descriptive messages.
5. Push your changes to your forked repository.
6. Submit a pull request detailing your changes.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

The Driving License Detection system is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [YOLO (You Only Look Once)](https://pjreddie.com/darknet/yolo/) for real-time object detection.
- [OpenAIVision](https://openai.com/) for enhanced image processing and vision capabilities.
- [OpenCV](https://opencv.org/) for computer vision functions.

For more information, visit the [GitHub repository](https://github.com/pr0fi7/driving_licence_detection).
