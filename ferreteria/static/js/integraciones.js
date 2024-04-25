function obtenerValor() {
    var usd = $('#usd').val();
    ({
        url: '/converter',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({usd: usd}),
        success: function(response) {
            $('.converter-input[disabled]').val(response.convertido);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}