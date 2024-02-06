
///--Get the selector button for handle the grafic
document.getElementById('tuBoton').addEventListener('click', function() {
    // Realize HttpRequest REQUEST
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/generate_plot/', true);

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            // Success in the request, update the content with the graph
            let response = JSON.parse(xhr.responseText);
            let img = new Image();
            img.src = 'data:image/png;base64,' + response.image;
            document.getElementById('contenedorGrafico').appendChild(img);
        } else {
            // Errors
            console.error('Error en la solicitud AJAX');
        }
    };

    xhr.onerror = function() {
        // Errors in red
        console.error('Error de red');
    };

    // Send the request
    xhr.send();
});
