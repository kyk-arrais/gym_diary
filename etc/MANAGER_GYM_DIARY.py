import json
from datetime import datetime

# Dicionário centralizado com suporte a multi-idioma para os dias
IDIOMAS = {
    "en": {
        "Monday": "MONDAY",
        "Tuesday": "TUESDAY",
        "Wednesday": "WEDNESDAY",
        "Thursday": "THURSDAY",
        "Friday": "FRIDAY",
        "Saturday": "SATURDAY",
        "Sunday": "SUNDAY"
    },
    "pt": {
        "Monday": "SEGUNDA-FEIRA",
        "Tuesday": "TERÇA-FEIRA",
        "Wednesday": "QUARTA-FEIRA",
        "Thursday": "QUINTA-FEIRA",
        "Friday": "SEXTA-FEIRA",
        "Saturday": "SÁBADO",
        "Sunday": "DOMINGO"
    }
}

def load_routine():
    """Carrega a rotina do arquivo JSON ou retorna a estrutura inicial vazia."""
    name_file = "routine_config.json"
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "Monday": {"block": "", "exercises": []},
            "Tuesday": {"block": "", "exercises": []},
            "Wednesday": {"block": "", "exercises": []},
            "Thursday": {"block": "", "exercises": []},
            "Friday": {"block": "", "exercises": []},
            "Saturday": {"block": "", "exercises": []},
            "Sunday": {"block": "", "exercises": []}
        }

def save_routine(new_routine):
    """Salva a estrutura atual de treinos no JSON."""
    name_file = "routine_config.json"
    with open(name_file, "w", encoding="utf-8") as file:
        json.dump(new_routine, file, indent=4, ensure_ascii=False)

def date_update():
    """Retorna a data e hora atual formatada."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def saving_historic(exercise_name, weight, rep, block_train):
    """Guarda a execução de um exercício específico no histórico."""
    name_file = "TrainManagerHistory.json"
    train_data_file = {
        "data": date_update(),
        "bloco": block_train,
        "exercicio": exercise_name,
        "carga": weight,
        "repeticoes": rep
    }
     
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            history = json.load(file)   
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    history.append(train_data_file)

    with open(name_file, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)
        print("Saved")