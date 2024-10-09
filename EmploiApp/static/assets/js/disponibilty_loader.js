document.addEventListener('DOMContentLoaded', function () {
    const professeurField = document.getElementById('id_professeur');  // Champ Professeur
    const profDispoField = document.getElementById('id_profDispoWeek');  // Champ Disponibilités Professeur

    // Fonction pour mettre à jour les plages horaires via AJAX
    function updateProfDispoOptions(professeurId) {
        if (!professeurId) {
            profDispoField.innerHTML = '';  // Vide les options si aucun professeur n'est sélectionné
            return;
        }

        // Requête AJAX pour obtenir les plages horaires du professeur sélectionné
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `/admin/get_prof_dispo/?professeur_id=${professeurId}`, true);  // On change ici pour professeur_id
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 400) {
                const response = JSON.parse(xhr.responseText);
                profDispoField.innerHTML = '';  // Vide le champ actuel
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

    // Écoute le changement du champ `professeur`
    professeurField.addEventListener('change', function () {
        const professeurId = this.value;
        updateProfDispoOptions(professeurId);  // On envoie maintenant l'ID du professeur
    });

    // Mise à jour initiale si un professeur est déjà sélectionné lors du chargement
    if (professeurField.value) {
        updateProfDispoOptions(professeurField.value);
    }
});
