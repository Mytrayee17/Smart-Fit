# image_processing.py

import cv2
import mediapipe as mp
import math


def calculate_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def process_image(image_path, ref_length_in, ref_width_in):
    """Processes the image to extract measurements using the reference object."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error loading image.")
        return None

    # Step 1: Prompt user to select the four corners of the reference object
    ref_points = get_reference_object_points(image)
    if len(ref_points) != 4:
        print("Error: Four points for the reference object not provided.")
        return None

    # Step 2: Calculate the reference object's pixel length and width
    ref_length_px = calculate_distance(ref_points[0], ref_points[1])
    ref_width_px = calculate_distance(ref_points[1], ref_points[2])

    # Step 3: Calculate Pixels Per Inch (PPI)
    ppi_length = ref_length_px / ref_length_in
    ppi_width = ref_width_px / ref_width_in
    ppi = (ppi_length + ppi_width) / 2  # Average PPI

    # Initialize MediaPipe Pose for detecting human landmarks
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        if not results.pose_landmarks:
            print("No landmarks detected.")
            return None

        landmarks = results.pose_landmarks.landmark

        # Calculate chest, waist, and hips measurements using PPI

        # Chest/Bust measurement: Distance between left and right shoulder
        shoulder_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        chest_width_pixels = calculate_distance(
            (shoulder_left.x * image.shape[1], shoulder_left.y * image.shape[0]),
            (shoulder_right.x * image.shape[1], shoulder_right.y * image.shape[0])
        )
        chest_width_inches = chest_width_pixels / ppi

        # Waist measurement: Distance between left and right hip
        hip_left = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        hip_right = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        waist_width_pixels = calculate_distance(
            (hip_left.x * image.shape[1], hip_left.y * image.shape[0]),
            (hip_right.x * image.shape[1], hip_right.y * image.shape[0])
        )
        waist_width_inches = waist_width_pixels / ppi

        # Hips measurement: Distance between the outermost points of the hip landmarks
        hips_width_inches = waist_width_inches

        # Compile measurements in inches
        measurements = {
            "Chest/Bust": chest_width_inches,
            "Waist": waist_width_inches,
            "Hips": hips_width_inches,
        }

        return measurements


def get_reference_object_points(image):
    """Allows the user to click four points representing the reference object's corners."""
    ref_points = []

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(ref_points) < 4:
                ref_points.append((x, y))
                print(f"Reference point {len(ref_points)}: ({x}, {y})")
            if len(ref_points) == 4:
                cv2.destroyAllWindows()

    # Display the image and set mouse callback
    cv2.imshow("Select Reference Object Corners", image)
    cv2.setMouseCallback("Select Reference Object Corners", mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return ref_points
