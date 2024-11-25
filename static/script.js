/*
Questo file JavaScript gestisce la logica lato client. Le sue responsabilità principali sono:

Gestione del modulo di input:
        Aggiunge un evento al pulsante "Calcola" per intercettare l'invio del modulo.
        Legge i valori inseriti dall'utente (città e data).

Invio della richiesta API:
        Effettua una chiamata HTTP GET all'endpoint /api/calculate con i parametri city e date.
        Riceve la risposta dal server in formato JSON.

Aggiornamento dinamico dell'interfaccia utente:
        Mostra i risultati della richiesta (data, città, alba, tramonto, festività).
        Gestisce eventuali errori mostrando un messaggio all'utente.
 */

document.getElementById('form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const city = document.getElementById('city').value;
    const date = document.getElementById('date').value;

    if (!city || !date) {
        alert("Inserisci tutti i campi!");
        return;
    }

    // invia una richiesta API GET a /api/calculate con i parametri
    const response = await fetch(`/api/calculate?city=${encodeURIComponent(city)}&date=${encodeURIComponent(date)}`);
    const data = await response.json();

    if (response.ok) {
        document.getElementById('result').innerHTML = `
            <h2>Risultati</h2>
            <p><strong>Data:</strong> ${data.sun_times.data}</p>
            <p><strong>Città:</strong> ${data.sun_times.città}</p>
            <p><strong>Alba:</strong> ${data.sun_times.alba}</p>
            <p><strong>Tramonto:</strong> ${data.sun_times.tramonto}</p>
            <p><strong>È festivo?:</strong> ${data.holiday_info.festivo ? 'Sì' : 'No'}</p>
            ${data.holiday_info.nome_festivo ? `<p><strong>Nome festività:</strong> ${data.holiday_info.nome_festivo}</p>` : ''}
        `;
    } else {
        document.getElementById('result').innerHTML = `<p style="color: red;">Errore: ${data.error}</p>`;
    }
});
