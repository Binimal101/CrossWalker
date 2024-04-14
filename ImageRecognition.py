import Camera
import cv2
import numpy as np

isInStreetCenter = False
light_forward = True
light_side = False


def getCommand(moving_vehicles, stationary_people):
    global light_forward, light_side, isInStreetCenter
   
    any_vehicle_moving = any(count > 0 for count in moving_vehicles.values())

    # Check conditions and return corresponding commands
    if light_forward and not light_side:
        if not any_vehicle_moving:
            if stationary_people > 0:
                if not isInStreetCenter:
                    isInStreetCenter = True
                    return "FORWARD"
            elif stationary_people == 0 and isInStreetCenter:
                isInStreetCenter = False
                return "BACKWARD"
        else:
            if stationary_people > 0:
                return "DO NOTHING"

    elif not light_forward and light_side:
        light_forward = True
        light_side = False
        return "ROTATE 90"

    # If no other condition is met
    return "DO NOTHING"



def analyze(frame, model, prev_boxes):
    """
    Analyzes the frame to detect moving specified vehicles and stationary people.
    """
    
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    model.setInput(blob)
    detections = model.forward()

    # Define vehicle types to track
    vehicle_types = ['car', 'bus', 'bicycle', 'motorbike']
    moving_vehicles = {vehicle: 0 for vehicle in vehicle_types}
    stationary_people = 0
    current_boxes = {}

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:  # Lowered confidence threshold for better detection coverage
            idx = int(detections[0, 0, i, 1])
            class_name = classes[idx]

            if class_name in vehicle_types or class_name == "person":
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")

                # Draw bounding box and label on the frame
                label = f"{class_name}: {confidence:.2f}"
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Manage bounding boxes for comparison
                current_boxes[class_name] = (startX, startY, endX, endY)

                # Movement detection
                if class_name in prev_boxes and prev_boxes[class_name] is not None:
                    prev_box = prev_boxes[class_name]
                    box_movement = np.linalg.norm(np.array(prev_box[:2]) - np.array([startX, startY]))

                    if box_movement > 3:  # Movement threshold
                        if class_name in vehicle_types:
                            moving_vehicles[class_name] += 1
                    
                    if class_name == "person":
                        stationary_people += 1

    return moving_vehicles, stationary_people, current_boxes
recentAnalysis = analysisStack.pop()
previousAnaysis = analysisStack.pop()
