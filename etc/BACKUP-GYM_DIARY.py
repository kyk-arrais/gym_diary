import json
from datetime import datetime
from TreinoCLS import Exercises

BANK_EXERCISES = [
     "Supino reto na barra",
     "Supino reto c/ Halteres",
     "Supino inclinado na barra",
     "Supino inclinado c/ Halteres",
     "Supino declinado na barra",
     "Supino declinado c/ Halteres",
     "Ombro lateral Polia",
     "Ombro lateral c/ Halteres",
     "Ombro frontal Polia",
     "Ombro frontal c/ Halteres",
     "Ombro posterior Polia",
     "Ombro posterior Halteres"
]

ROUTINE_WEEK = {
    "Monday": "PUSH",
    "Tuesday": "PULL",
    "Wednesday": "LEGS",
    "Thursday": "PUSH",
    "Friday": "PULL",
    "Saturday": "LEGS",
    "Sunday": "DESCANSO"
}

DIAS_TRADUZIDOS = {
    "Monday": "SEGUNDA-FEIRA",
    "Tuesday": "TERÇA-FEIRA",
    "Wednesday": "QUARTA-FEIRA",
    "Thursday": "QUINTA-FEIRA",
    "Friday": "SEXTA-FEIRA",
    "Saturday": "SÁBADO",
    "Sunday": "DOMINGO"
}

def load_routine():
    name_file = "routine_config.json"

    try:
        with open(name_file, "r", encoding="utf-8") as file:
            return(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "Monday": "PUSH",
            "Tuesday": "PULL",
            "Wednesday": "LEGS",
            "Thursday": "PUSH",
            "Friday": "PULL",
            "Saturday": "LEGS",
            "Sunday": "DESCANSO"
        }

def save_routine(new_routine):
    name_file = "routine_config.json"

    with open(name_file, "w", encoding="utf-8") as file:
        json.dump(new_routine, file, indent=4, ensure_ascii=False)

def date_update():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M")

def search_suggestions(text_suggestions):
    term = text_suggestions.lower()

    suggestions = [exe for exe in BANK_EXERCISES if term in exe.lower()]
    return suggestions

def get_train_day():
    day = datetime.now().strftime("%A")
    name_day_pt = DIAS_TRADUZIDOS.get(day, "DESCONHECIDO")
    current_routine = load_routine()
    division = current_routine.get(day, "LIVRE")

    return name_day_pt, division

def saving_historic(obj_exe, date_str, block_train):
    name_file = "TrainManagerHistory.json"

    train_data_file = {
        "data": date_str,
        "bloco": block_train,
        "exercicio": obj_exe.name,
        "carga": obj_exe.weight,
        "repeticoes": obj_exe.rep
    }
     
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            history = json.load(file)   
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    history.append(train_data_file)

    with open(name_file, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

        print("Treino guardado com sucesso no histórico!")
     
def main():
    day, block = get_train_day()
    print(f"=== {day} ({block}) ===")

    if block == "DESCANSO":
        print("Hoje é dia de descanso! Foque na recuperação.")
        return
    
    typing = input("\nExercicio: ")
    options = search_suggestions(typing)
    try:
        if not options:
            final_type = typing
        else:
            for i, option in enumerate(options, 1):
                print(f"[{i}] {option}")

            pick_exe = int(input("Escolha o número do exercício: "))
            final_type = options[pick_exe - 1]

        print(f"{final_type}")
        weight = float(input("Kg: "))
        rep = int(input("Rep: "))

        save_train = Exercises(final_type, weight, rep)
        weight_date = date_update()

        print(f"{save_train} \n{weight_date}")

        saving_historic(save_train, weight_date, block)

    except (ValueError, IndexError): 
        print("Opção inválida.")

if __name__ == "__main__":
     main()