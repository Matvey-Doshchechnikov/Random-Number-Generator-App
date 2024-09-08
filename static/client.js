document.addEventListener('DOMContentLoaded', function() {
    function fetchNumber() {
        fetch('/number')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Ошибка:', data.error);
                } else {
                    document.getElementById('number').textContent = data.number;
                }
            })
            .catch(error => console.error('Ошибка запроса:', error));
    }
    setInterval(fetchNumber, 5000);
    fetchNumber();
});
