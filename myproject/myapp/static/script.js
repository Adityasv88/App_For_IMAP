document.addEventListener('DOMContentLoaded', function() {
    // Get the form and processed image container
    const imageForm = document.getElementById('image-form');
    const processedImageContainer = document.getElementById('processed-image');

    // Handle form submission
    imageForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get the selected processing option and uploaded image
        const processingOption = document.getElementById('processing-option').value;
        const imageInput = document.getElementById('image-upload');
        const imageFile = imageInput.files[0];

        // Create FormData object to send data with AJAX
        const formData = new FormData();
        formData.append('image', imageFile);

        // Make an AJAX request based on the selected processing option
        let url = '';
        switch (processingOption) {
            case 'sharpen':
                url = '/myapp/sharpen/';
                break;
            case 'array':
                url = '/myapp/image_to_dataframe/';
                break;
            case 'resize':
                url = '/myapp/resize/';
                break;
            default:
                console.error('Invalid processing option');
                return;
        }

        // Make a POST request to the corresponding Django view
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response based on the processing option
            switch (processingOption) {
                case 'sharpen':
                    // Process the sharpened image and update the DOM
                    const sharpenedImage = data.result;
                    processedImageContainer.innerHTML = `<img src="data:image/jpeg;base64,${sharpenedImage}" alt="Processed Image" class="img-fluid" />`;
                    break;
                case 'array':
                    // Process the image data to a DataFrame and update the DOM
                    const dataframe = JSON.parse(data.dataframe);
                    const table = generateDataTable(dataframe);
                    processedImageContainer.innerHTML = table;
                    break;
                case 'resize':
                    // Process the resized image and update the DOM
                    const resizedImage = data.result;
                    processedImageContainer.innerHTML = `<img src="data:image/jpeg;base64,${resizedImage}" alt="Processed Image" class="img-fluid" />`;
                    break;
            }
        })
        .catch(error => console.error(error));
    });

    // Helper function to generate a data table from DataFrame data
    function generateDataTable(dataframe) {
        let tableHTML = '<table class="table"><thead><tr>';
        // Extract column names
        const columns = Object.keys(dataframe[0]);
        // Add column headers to the table
        columns.forEach(column => {
            tableHTML += `<th>${column}</th>`;
        });
        tableHTML += '</tr></thead><tbody>';
        // Add rows to the table
        dataframe.forEach(row => {
            tableHTML += '<tr>';
            columns.forEach(column => {
                tableHTML += `<td>${row[column]}</td>`;
            });
            tableHTML += '</tr>';
        });
        tableHTML += '</tbody></table>';
        return tableHTML;
    }
});
