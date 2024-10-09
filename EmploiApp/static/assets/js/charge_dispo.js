document.addEventListener('DOMContentLoaded', function () {
    console.log('Le script est chargé');
    const professeurField = document.getElementById('id_professeur');
    console.log('Element professeurField:', professeurField);
    const profDispoField = document.getElementById('id_profDispoWeek');

    function updateProfDispoOptions(professeurId) {
        console.log('Envoi de la requête pour le professeur ID :', professeurId);
        if (!professeurId) {
            profDispoField.innerHTML = '';
            return;
        }

        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/admin/get_prof_dispo/?professeur_id=${professeurId}`, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 400) {
                const response = JSON.parse(xhr.responseText);
                profDispoField.innerHTML = '';
                response.forEach(function (option) {
                    const newOption = document.createElement('option');
                    newOption.value = option.id;
                    newOption.text = option.text;
                    profDispoField.appendChild(newOption);
                });
            } else {
                console.error('Erreur lors de la récupération des données');
            }
        };

        xhr.onerror = function () {
            console.error('Erreur réseau lors de la requête AJAX');
        };

        xhr.send();
    }

    professeurField.addEventListener('change', function () {
        const professeurId = this.value;
        console.log('Changement du professeur ID :', professeurId);
        updateProfDispoOptions(professeurId);
    });

    if (professeurField.value) {
        updateProfDispoOptions(professeurField.value);
    }
});
