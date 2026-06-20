import numpy as np
from music21 import converter, note, chord, stream
import customtkinter as ctk
import tensorflow as tf
import subprocess
import threading

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

files = [
    "data_set/1.mid","data_set/2.mid","data_set/3.mid","data_set/4.mid","data_set/5.mid",
    "data_set/6.mid","data_set/7.mid","data_set/8.mid","data_set/9.mid","data_set/10.mid",
    "data_set/11.mid","data_set/12.mid","data_set/13.mid","data_set/14.mid","data_set/15.mid",
    "data_set/16.mid","data_set/17.mid","data_set/18.mid","data_set/19.mid","data_set/20.mid"
]

def sample_with_temperature(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)

def start():

    def run_training():

        notes = []

        for file in files:
            midi = converter.parse(file)
            for element in midi.flatten().notes:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n.pitch.midi) for n in element.notes))

        pitchnames = sorted(set(notes))
        note_to_int = {n: i for i, n in enumerate(pitchnames)}

        network_input = [note_to_int[n] for n in notes]

        sequence_length = 100
        x, y = [], []

        for i in range(len(network_input) - sequence_length):
            x.append(network_input[i:i + sequence_length])
            y.append(network_input[i + sequence_length])

        x = np.array(x)
        y = tf.keras.utils.to_categorical(y)

        x = np.reshape(x, (x.shape[0], x.shape[1], 1))
        x = x / float(len(pitchnames))

        model = tf.keras.Sequential([
            tf.keras.Input(shape=(x.shape[1], x.shape[2])),
            tf.keras.layers.LSTM(256, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(256),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(y.shape[1], activation="softmax")
        ])

        model.compile(loss='categorical_crossentropy', optimizer='adam')

        model.fit(x, y, epochs=20, batch_size=16)

        model.save("music_model.keras")

        generated = []
        start_pattern = x[np.random.randint(0, len(x) - 1)]
        pattern = start_pattern.flatten()

        for _ in range(300):
            x_input = pattern.reshape(1, len(pattern), 1)
            prediction = model.predict(x_input, verbose=0)
            index = sample_with_temperature(prediction[0], temperature=1.2)
            generated.append(index)
            pattern = np.append(pattern[1:], index)

        notes_output = [pitchnames[i] for i in generated]

        output = stream.Stream()

        for n in notes_output:
            if "." in n:
                c = chord.Chord([int(x) for x in n.split(".")])
                output.append(c)
            else:
                output.append(note.Note(n))

        output.write('midi', fp="generated_music.mid")

        print("generated")
        print("x shape:", x.shape)
        print("y shape:", y.shape)

    threading.Thread(target=run_training, daemon=True).start()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("music generator")
app.geometry("1000x1000")

label = ctk.CTkLabel(app, text="Welcome to music generator", font=("Arial", 30))
label.place(x=260, y=30)

file_path = r"D:\music_project\generated_music.mid"

def open_file():
    subprocess.run(["explorer.exe", "/mnt/d/music_project/generated_music.mid"])

button = ctk.CTkButton(app, text="generate Music", font=("Arial", 20), command=start)
button.place(x=500, y=300)

button1 = ctk.CTkButton(app, text="open file", font=("Times New Roman", 30), command=open_file)
button1.place(x=300, y=700)

app.mainloop()
