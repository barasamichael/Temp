document.querySelector('#registration-form').addEventListener('submit', function (e) {
	e.preventDefault();

	fetch('/api/v1/register_user', {
		method: 'POST',
		body: new FormData(this),
	})
		.then(response => response.json())
		.then(data => {
			showAlert(data.message);

			if (data.message === 'User registered successfully') {
				window.location.href = '/profiles/dashboard';
			}
		})
		.catch(error => {
			console.error(error);
			showAlert('Registration failed', 'error');
		});
});

function showAlert(message, type = 'success') {
	const alertElement = document.querySelector('#alertMessage');
	alertElement.innerText = message;
	alertElement.className = `alert ${type} p-3 mb-6`;
	alertElement.style.display = 'block';

	setTimeout(() => {
		alertElement.style.display = 'none';
	}, 10000);
}
