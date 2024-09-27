import base64
import requests
import cv2
import math
import os
import xlsxwriter
from io import BytesIO
import ast
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openaiapi = os.getenv("OPENAI_API_KEY")

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def resize_and_encode_image(image, max_width=None, max_height=None):
    # Resize the image while maintaining aspect ratio
    height, width = image.shape[:2]

    if max_width is not None and width > max_width:
        new_width = max_width
        new_height = int(height * (max_width / width))
    elif max_height is not None and height > max_height:
        new_height = max_height
        new_width = int(width * (max_height / height))
    else:
        new_width, new_height = width, height

    resized_image = cv2.resize(image, (new_width, new_height))

    # Encode the resized image to PNG format in memory
    _, encoded_image = cv2.imencode('.png', resized_image)

    return BytesIO(encoded_image.tobytes())



def write_csv(index, date, time, place, license_plates_images, output_path):
    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet()

    worksheet.set_column('B:B', 20)
    worksheet.set_column('E:E', 20)

    worksheet.write(0, 1, 'Date')
    worksheet.write(0, 2, 'Time')
    worksheet.write(0, 3, 'Place')
    worksheet.write(0, 4, 'License Plate')
    worksheet.write(0, 5, 'Image')

    for license_plate, image in license_plates_images:
        worksheet.set_row(index, 50)
        worksheet.write(index, 1, date)
        worksheet.write(index, 2, time)
        worksheet.write(index, 3, place)
        worksheet.write(index, 4, license_plate)

        image_stream = resize_and_encode_image(image, max_width=50, max_height=50)

        worksheet.insert_image(index, 5, '', {'image_data': image_stream, 'x_scale': 1, 'y_scale': 1})

        index += 1

    workbook.close()




def video_to_images(video_path, frames_per_second=1):
    cam = cv2.VideoCapture(video_path)
    frame_list = []
    frame_rate = cam.get(cv2.CAP_PROP_FPS)

    current_frame = 0

    images_path = './data/images'
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    if frames_per_second > frame_rate or frames_per_second == -1:
        frames_per_second = frame_rate

    while True:
        ret, frame = cam.read()

        if ret:
            file_name = f'{images_path}/frame{current_frame}.jpg'
            print('Creating...' + file_name)

            if current_frame % (math.floor(frame_rate / frames_per_second)) == 0:
                frame_list.append(frame)
                cv2.imwrite(file_name, frame)

            current_frame += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()

    return frame_list

def detect_text(images):
    api_key = openaiapi

    converted_images = []

    for image in images:
        _, buffer = cv2.imencode('.jpg', image)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        converted_images.append(base64_image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    image_payload = [
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        for base64_image in converted_images
    ]

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s the text on these license plate images? Provide the text only for license plates that are clearly visible and that you are confident in. Mind general format of license plates: length, symbols, etc. Format your response as a python list: ['text1', 'text2', 'text3']. Don't put the same plate or highly possibly the same plate twice. In the end, separately: if you skipped some images meaning that they probably are not licence plates, return their index, starting from 0, of images that you have skipped. Write in the following format 'Skipped': []"
                    },
                    *image_payload
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']

def format_license_plates_and_skipped(plates_str):
    # Split the plates string to separate the actual plates and the skipped indices
    plates_str, skipped_str = plates_str.split("Skipped:")
    plates_str = plates_str.strip().strip("```python").strip().strip("```")
    
    try:
        plates_list = ast.literal_eval(plates_str)
        skipped_list = ast.literal_eval(skipped_str.strip())
    except Exception as e:
        print(f"Error parsing the list: {e}")
        return [], []
    
    formatted_plates = []
    for plate in plates_list:
        if any(char.isdigit() for char in plate) and any(char.isalpha() for char in plate):
            formatted_plates.append(plate.strip())
    
    # Remove duplicates
    formatted_plates = list(dict.fromkeys(formatted_plates))

    return formatted_plates, skipped_list