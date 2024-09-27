from ultralytics import YOLO
import cv2
import supervision as sv
import matplotlib.pyplot as plt
from datetime import datetime
from util import write_csv, video_to_images, detect_text, format_license_plates_and_skipped, chunker


detections_ = {}
mot_tracker = sv.ByteTrack()

license_plate_detector = YOLO('/content/drive/MyDrive/licence_plates.pt')

frame_list = video_to_images('/content/drive/MyDrive/2024-07-29 13.43.48.mp4', frames_per_second=8)

license_plates_images = []

for frame_nmr, frame in enumerate(frame_list):
    detections = license_plate_detector(frame)[0]
    detection_supervision = sv.Detections.from_ultralytics(detections)
    detections_with_tracks = mot_tracker.update_with_detections(detection_supervision)
    print(detections_with_tracks)

    for frame_detection in detections_with_tracks:
        bbox = frame_detection[0].tolist()
        track_id = frame_detection[4]
        score = frame_detection[2]
        x1, y1, x2, y2 = bbox

        if track_id not in detections_:
            detections_[track_id] = {'frame': frame_nmr, 'bbox': [x1, y1, x2, y2], 'score': score}
        else:
            if score > detections_[track_id]['score']:
                detections_[track_id] = {'frame': frame_nmr, 'bbox': [x1, y1, x2, y2], 'score': score}

print(detections_)

images = []
for license_id, info in detections_.items():
    frame_nmr = info['frame']
    x1, y1, x2, y2, score = info['bbox'][0], info['bbox'][1], info['bbox'][2], info['bbox'][3], info['score']
    frame = frame_list[frame_nmr]
    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]
    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

    images.append(license_plate_crop_gray)

formatted_licenses = []
all_skipped_images = []

for image_batch in chunker(images, 10):
    text = detect_text(image_batch)
    print(text)
    licenses, skipped = format_license_plates_and_skipped(text)
    formatted_licenses.extend(licenses)
    all_skipped_images.extend(skipped)

good_images = [img for i, img in enumerate(images) if i not in all_skipped_images]

# Pair the formatted licenses with their corresponding good images
license_plates_images = list(zip(formatted_licenses, good_images))

# Ensure that the number of licenses matches the number of images
if len(formatted_licenses) != len(good_images):
    print("Warning: The number of formatted licenses does not match the number of images.")

# Continue with writing to the Excel file as before
current_datetime = datetime.now()
date_str = current_datetime.strftime("%Y-%m-%d")
time_str = current_datetime.strftime("%H:%M:%S")

write_csv(1, date_str, time_str, 'Some Location', license_plates_images, f'./license_plates_{date_str}_{time_str}.xlsx')

# Optionally, show images to confirm they're correct
for image in good_images:
    plt.imshow(image, cmap='gray')
    plt.show()
