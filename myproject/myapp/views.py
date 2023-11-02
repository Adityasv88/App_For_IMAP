# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render


# def my_view(request):

#     return render(request, 'my_view.html')
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import pandas as pd
import numpy as np

# Django view for rendering the HTML template


def my_view(request):
    return render(request, 'my_view.html')

# Django view for image sharpening


@csrf_exempt
def sharpen_image(request):
    if request.method == 'POST':
        # Get image data from POST request
        image_data = request.POST.get('image_data')

        # Perform image sharpening logic using OpenCV
        image_bytes = np.frombuffer(bytes.fromhex(image_data), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

        if image is not None:
            # Perform image sharpening (Example: using unsharp masking)
            sharpened_image = cv2.GaussianBlur(image, (0, 0), 3)
            sharpened_image = cv2.addWeighted(
                image, 1.5, sharpened_image, -0.5, 0)

            # Convert the sharpened image to a hex string
            sharpened_image_hex = sharpened_image.tobytes().hex()
            return JsonResponse({'result': sharpened_image_hex})
        else:
            return JsonResponse({'error': 'Invalid image data'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# Django view for image resizing


@csrf_exempt
def resize_image(request):
    if request.method == 'POST':
        # Get image data from POST request
        image_data = request.POST.get('image_data')

        # Perform image resizing logic using OpenCV
        image_bytes = np.frombuffer(bytes.fromhex(image_data), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

        if image is not None:
            # Perform image resizing (Example: resizing to half the original size)
            resized_image = cv2.resize(
                image, (image.shape[1]//2, image.shape[0]//2))

            # Convert the resized image to a hex string
            resized_image_hex = resized_image.tobytes().hex()
            return JsonResponse({'result': resized_image_hex})
        else:
            return JsonResponse({'error': 'Invalid image data'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# Django view for converting image to a dataframe and returning it as JSON


@csrf_exempt
def image_to_dataframe(request):
    if request.method == 'POST':
        # Get image data from POST request
        image_data = request.POST.get('image_data')

        # Perform image to dataframe logic using pandas
        image_bytes = np.frombuffer(bytes.fromhex(image_data), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

        if image is not None:
            # Convert the image to a numpy array and reshape to 1D
            image_array = np.array(image).reshape(-1)

            # Create a dictionary with column names and corresponding values
            data = {f'Pixel_{i+1}': [value]
                    for i, value in enumerate(image_array)}

            # Create a DataFrame from the dictionary
            df = pd.DataFrame(data)
            return JsonResponse({'dataframe': df.to_json(orient='records')})
        else:
            return JsonResponse({'error': 'Invalid image data'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
