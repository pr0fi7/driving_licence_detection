from io import BytesIO
import xlsxwriter
import cv2

# Read the image using OpenCV
file_name = 'data/images/frame8.jpg'
image = cv2.imread(file_name)

# Resize the image to make it smaller
new_width = 100  # Adjust the width as needed
new_height = int(image.shape[0] * (new_width / image.shape[1]))  # Preserve the aspect ratio
resized_image = cv2.resize(image, (new_width, new_height))

# Encode the resized image as a PNG in memory
_, encoded_image = cv2.imencode('.png', resized_image)

# Convert the encoded image to a BytesIO object
image_stream = BytesIO(encoded_image.tobytes())

# Create a new Excel file and add a worksheet
workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

# Insert the resized image into the worksheet
worksheet.insert_image('C5', file_name, {'image_data': image_stream})

# Close the workbook
workbook.close()
