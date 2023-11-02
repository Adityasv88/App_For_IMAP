document.addEventListener('DOMContentLoaded', function() {
    const imageForm = document.getElementById('image-form');
    const processedDataContainer = document.getElementById('processed-data');

    imageForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(imageForm);

        fetch('/myapp/image_to_dataframe/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                processedDataContainer.innerHTML = `<p class="text-danger">${data.error}</p>`;
            } else {
                const dataframe = JSON.parse(data.dataframe);
                const table = generateDataTable(dataframe);
                processedDataContainer.innerHTML = table;
            }
        })
        .catch(error => {
            processedDataContainer.innerHTML = `<p class="text-danger">Error occurred: ${error}</p>`;
        });
    });

    function generateDataTable(dataframe) {
        let tableHTML = '<table class="table"><thead><tr>';
        const columns = Object.keys(dataframe[0]);
        columns.forEach(column => {
            tableHTML += `<th>${column}</th>`;
        });
        tableHTML += '</tr></thead><tbody>';
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
