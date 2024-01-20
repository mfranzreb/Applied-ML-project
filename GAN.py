import tensorflow as tf
from tensorflow.keras import layers, models
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# 1. Daten laden und formatieren
# Verzeichnis mit den Daten
data_directory = r"C:\Users\gloom\Documents\GitHub\AML\data"

# Liste für Geometrie- und cd_cl-Dateien
geometry_files = []
cd_cl_files = []

# Durchsuche alle Ordner im Verzeichnis
for folder in os.listdir(data_directory):
    folder_path = os.path.join(data_directory, folder)
    
    # Überprüfe, ob es sich um einen Ordner handelt
    if os.path.isdir(folder_path):
        # Durchsuche die Dateien im Ordner
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            # Überprüfe, ob es sich um eine Geometrie- oder cd_cl-Datei handelt
            if file.endswith("coords.csv"):
                geometry_files.append(file_path)
            elif file.endswith("polar.csv"):
                cd_cl_files.append(file_path)

# Lese die Geometrie- und cd_cl-Daten ein
geometry_data_list = [pd.read_csv(file) for file in geometry_files]
cd_cl_data_list = [pd.read_csv(file) for file in cd_cl_files]

# Füge die Daten zusammen (abhängig von der Struktur deiner Daten)
merged_data_list = [pd.concat([geometry_data, cd_cl_data], axis=1) for geometry_data, cd_cl_data in zip(geometry_data_list, cd_cl_data_list)]

# Normalisiere die Daten (Beispiel)
scaler = MinMaxScaler()
normalized_data_list = [scaler.fit_transform(data) for data in merged_data_list]


# 2. Aufteilung in Trainings- und Testdaten
train_data_list, test_data_list = train_test_split(normalized_data_list, test_size=0.2, random_state=42)

# Extrahiere Geometrie- und cd_cl-Daten für Trainings- und Testdaten
X_train_list, y_train_list = zip(*train_data_list)
X_test_list, y_test_list = zip(*test_data_list)

# Konvertiere die Listen in NumPy-Arrays
X_train = pd.concat(X_train_list, axis=0).values
y_train = pd.concat(y_train_list, axis=0).values
X_test = pd.concat(X_test_list, axis=0).values
y_test = pd.concat(y_test_list, axis=0).values

# 3. Model erstellen
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(2,)),  # 2 für Cd und Cl
    layers.Dense(128, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(2)  # 2 für x und y Koordinaten der Profilgeometrie
])


# 4. Modell kompilieren
model.compile(optimizer='adam', loss='mse')


# 5. Modell trainieren
model.fit(X_train, y_train, epochs=100, batch_size=32)


# 6. Generiere neue Daten

def modify_cd_cl_data(cd_cl_data, modifications):
    # Hier werden die Änderungen an den Cd-Cl-Werten vorgenommen
    # modifications ist ein Dictionary, z.B.: {'index_1': (neuer_Cd_1, neuer_Cl_1), 'index_2': (neuer_Cd_2, neuer_Cl_2)}
    for index, (new_cd, new_cl) in modifications.items():
        cd_cl_data.at[index, 'Cd'] = new_cd
        cd_cl_data.at[index, 'Cl'] = new_cl
    return cd_cl_data

neuer_Cd_1, neuer_Cl_1 = -0.8, 0.05  # Setze die neuen Cd-Cl-Werte hier ein
neuer_Cd_2, neuer_Cl_2 = -0.8, 0.05
modifications = {'index_1': (neuer_Cd_1, neuer_Cl_1), 'index_2': (neuer_Cd_2, neuer_Cl_2)}
modified_cd_cl_data = modify_cd_cl_data(cd_cl_data, modifications)

# Generiere Geometrie basierend auf den modifizierten Cd-Cl-Daten
def generate_geometry(model, cd_cl_data):
    # Extrahiere Cd-Cl-Werte aus der Datenbank
    input_cd_cl = cd_cl_data[['Cd', 'Cl']].values

    # Normalisiere die Eingabedaten, falls erforderlich (abhängig von der Normalisierung während des Trainings)
    input_cd_cl_normalized = scaler.transform(input_cd_cl)  # Annahme: scaler wurde während des Trainings erstellt

    # Generiere die Geometrie
    generated_geometry = model.predict(input_cd_cl_normalized)

    return generated_geometry

generated_geometry = generate_geometry(model, modified_cd_cl_data)


#7. Erstelle einen gerichteten Graph
G = nx.DiGraph()

# Füge Knoten hinzu
for i, (x, y) in enumerate(generated_geometry):
    G.add_node(i, pos=(x, y))

# Füge Kanten hinzu (Beispiel: Verbinde jeden Knoten mit dem nächsten)
for i in range(len(generated_geometry) - 1):
    G.add_edge(i, i+1)

# Zeichne den Graph
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, font_weight='bold')
plt.show()