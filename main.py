import holidays
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from astral import  LocationInfo
from astral.sun import sun
from geopy.geocoders import Nominatim

app = Flask(__name__)

def holiday_verifier(data, nazione="IT"):
    """
    :param data: datetime, la nostra data
    :param nazione: codice ISO per il paese
    :return: dizionario con informazioni sulla festività
    """
    giorni_festivi = holidays.country_holidays(nazione)
    is_domenica = data.weekday() == 6
    is_festivo = data.date() in giorni_festivi or is_domenica
    nome_festivo = "Domenica" if is_domenica else giorni_festivi.get(data.date(), "Non festivo") if is_festivo else None

    return {
        "data": data.date(),
        "festivo": is_festivo,
        "nome_festivo": nome_festivo,
    }

def calculate_sun_times(data, city_name, timezone="Europe/Rome"):
    """
    Calcola gli orari di alba e tramonto per una data e una cittò

    :param data: datetime, la nostra data
    :param city_name: string, nome della città
    :param timezone: fuso orario
    :return: dizionario con orari di alba e tramonto
    """

    geolocator = Nominatim(user_agent="geoapiExcercises")
    location = geolocator.geocode(city_name)
    if not location:
        raise ValueError(f"Impossibile trovare la città: {city_name}")

    lat, lon = location.latitude, location.longitude
    city = LocationInfo("Location", "Country", timezone, lat, lon)
    sun_times = sun(city.observer, date=data.date(), tzinfo=city.timezone)
    alba = sun_times["sunrise"].strftime("%H:%M")
    tramonto = sun_times["sunset"].strftime("%H:%M")

    return {
        "data": data.date(),
        "città": city_name,
        "alba": alba,
        "tramonto": tramonto,
    }

@app.route('/')
def home():
    """
    Richiama la funzione home.
    Usa la funzione Flask render_template per caricare e restituire la pagina HTML index.html.
    Cerca il file index.html nella cartella templates/.
    """
    return render_template('index.html')

@app.route('/api/calculate', methods=['GET'])
def calculate():
    """
    La route /api/calculate è un endpoint che accetta richieste HTTP GET con parametri. Accetta SOLO richieste GET
    :return:
    """
    # Parametri dall'URL
    city_name = request.args.get('city')
    date_str = request.args.get('date')

    if not city_name or not date_str:
        return jsonify({"error": "Parametri 'city' e 'date' sono obbligatori."}), 400

    try:
        data = datetime.strptime(date_str, "%Y-%m-%d")

        holiday_result = holiday_verifier(data)
        sun_times_result = calculate_sun_times(data, city_name)

        result = {
            "holiday_info": holiday_result,
            "sun_times": sun_times_result
        }

        return jsonify(result)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Errore imprevisto: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
