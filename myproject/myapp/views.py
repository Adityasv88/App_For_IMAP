from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import pandas as pd
import numpy as np

# Django view for rendering the HTML template


def my_view(request):
    return render(request, 'my_view.html')

# Django view for converting image to a dataframe and returning it as JSON


@csrf_exempt
def image_to_dataframe(request):
    if request.method == 'POST':
        # Get image data from POST request
        image_data = request.FILES['image'].read()

        # Perform image to dataframe logic using OpenCV, pandas, and numpy
        image_np = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_UNCHANGED)

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
