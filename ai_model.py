# ai_model.py

def get_size_chart():
    """Returns predefined size charts for male and female users, including height, weight, chest/bust, waist, and hips."""
    return {
        "female": [
            {"Size": "XS", "Height": (60, 63), "Weight": (104, 119), "Chest/Bust": (30.5, 33), "Waist": (26, 27),
             "Hips": (32, 35)},
            {"Size": "S", "Height": (62, 65), "Weight": (115, 130), "Chest/Bust": (33.5, 35.5), "Waist": (27.6, 29.5),
             "Hips": (35.5, 38)},
            {"Size": "M", "Height": (63, 66), "Weight": (126, 141), "Chest/Bust": (36, 38), "Waist": (30, 32),
             "Hips": (38, 40)},
            {"Size": "L", "Height": (64, 68), "Weight": (137, 152), "Chest/Bust": (39, 41), "Waist": (33, 35.5),
             "Hips": (40.5, 42.5)},
            {"Size": "XL", "Height": (67, 69), "Weight": (159, 174), "Chest/Bust": (41, 43), "Waist": (36, 40),
             "Hips": (43, 45.5)},
            {"Size": "XXL", "Height": (68, 70), "Weight": (192, 207), "Chest/Bust": (43, 46), "Waist": (41, 44),
             "Hips": (45.5, 48)},
        ],
        "male": [
            {"Size": "XXS", "Height": (63, 66), "Weight": (119, 128), "Chest": (30, 32), "Waist": (24.5, 26),
             "Hips": (30.5, 32.5)},
            {"Size": "XS", "Height": (65, 68), "Weight": (123, 139), "Chest": (32, 34.5), "Waist": (26, 27.5),
             "Hips": (32.5, 35)},
            {"Size": "S", "Height": (67, 69), "Weight": (135, 150), "Chest": (34.5, 38), "Waist": (28, 30),
             "Hips": (35.5, 38)},
            {"Size": "M", "Height": (69, 71), "Weight": (146, 161), "Chest": (38, 41), "Waist": (30, 33.5),
             "Hips": (38, 40)},
            {"Size": "L", "Height": (70, 80), "Weight": (168, 187), "Chest": (41.5, 45), "Waist": (34, 37.5),
             "Hips": (40.5, 42.5)},
            {"Size": "XL", "Height": (72, 75), "Weight": (190, 209), "Chest": (45.5, 48), "Waist": (38, 41.5),
             "Hips": (43, 45.5)},
            {"Size": "XXL", "Height": (74, 76), "Weight": (221, 232), "Chest": (49, 52), "Waist": (41.5, 55),
             "Hips": (45.5, 48)},
        ]
    }


def is_in_range(value, range_tuple):
    """Helper function to check if a value falls within a given range tuple (min, max)."""
    if value is None:
        return False
    return range_tuple[0] <= value <= range_tuple[1]


def recommend_size(gender, measurements):
    """Recommends a clothing size based on gender and measurements, including height, weight, chest/bust, waist, and hips."""
    size_charts = get_size_chart()
    user_chart = size_charts.get(gender)

    if not user_chart:
        return "Size chart not available for the specified gender."

    # Check for missing measurements
    required_keys = ["Height", "Weight", "Chest/Bust" if gender == "female" else "Chest", "Waist", "Hips"]
    missing_keys = [key for key in required_keys if measurements.get(key) is None]

    if missing_keys:
        return f"Missing measurements for: {', '.join(missing_keys)}. Please try again."

    for size_info in user_chart:
        match = (
                is_in_range(measurements.get("Height"), size_info["Height"]) and
                is_in_range(measurements.get("Weight"), size_info["Weight"]) and
                is_in_range(measurements.get("Chest/Bust") if gender == "female" else measurements.get("Chest"),
                            size_info["Chest/Bust" if gender == "female" else "Chest"]) and
                is_in_range(measurements.get("Waist"), size_info["Waist"]) and
                is_in_range(measurements.get("Hips"), size_info["Hips"])
        )
        if match:
            return size_info["Size"]

    return "Size exceeds available range. Please consult a specialist."
