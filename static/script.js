document.getElementById('predictionForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById('loader').classList.remove('hidden');
    this.submit();
});
