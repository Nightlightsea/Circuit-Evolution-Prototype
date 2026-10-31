import threading
import pickle
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


from simulation.Evaluation import circuit_run_truth_table
from simulation.EvolutionSimulation import prepare_first_generations, run_simulation, prepare_next_generation
from simulation.Species import Species
from truth_tables import TestTables
from truth_tables.TruthTableLoader import load_truth_table


class Gui:
    def __init__(self, master):
        self.master = master
        self.running = False  # Initial state: not running
        self.worker_thread = None # To keep a reference to the thread
        self.truth_table = TestTables.mul_2
        self.generation_number = 0
        self.best_history = {}
        self.gene_pool: list[Species] = prepare_first_generations(self.truth_table, self.generation_number)
        self.size_penalty: bool = False

        self.fig, self.ax = plt.subplots()

        self.frame1 = tk.LabelFrame(self.master, text="Gene Pool", padx=10, pady=10)
        self.frame1.pack(side="left", fill="y")

        self.frame2 = tk.Frame(self.master, padx=10, pady=10)
        self.frame2.pack(side="left" ,fill="y", expand=True)

        self.subframe1 = tk.LabelFrame(self.frame2, padx=10, pady=10)
        self.subframe1.pack(side="top", fill="x", expand=True)

        canvas = FigureCanvasTkAgg(self.fig, master=self.subframe1)
        canvas.get_tk_widget().pack(expand=True)

        self.subframe2 = tk.LabelFrame(self.frame2, padx=10, pady=10)
        self.subframe2.pack(side="bottom", fill="x", expand=True)

        self.text_box_anatomy = tk.Text(self.subframe2, height=15, width=80)
        self.text_box_anatomy.pack(expand=True)

        self.frame3 = tk.LabelFrame(self.master, text="buttons", padx=5, pady=5)
        self.frame3.pack(side="right", fill="y")

        # text box
        self.text_box = tk.Text(self.frame1, height=50, width=30)
        self.text_box.pack()

        # open button
        self.open_button = tk.Button(
            self.frame3,
            text='Open a File',
            command=self.select_file
        )
        self.open_button.pack(pady=5)

        # Start Button
        self.start_button = tk.Button(self.frame3, text="Start simulation", width=15, command=self.start_simulation_process, state="normal")
        self.start_button.pack(pady=2)

        # Stop Button
        self.stop_button = tk.Button(self.frame3, text="Pause simulation", width=15, command=self.stop_simulation_process, state="disabled")
        self.stop_button.pack(pady=2)

        # Penalty Button
        self.penalty_button = tk.Button(self.frame3, text="Size Penalty off", width=15, command=self.size_penalty_switch, state="disabled")
        self.penalty_button.pack(pady=2)

        # Save Gene Pool
        self.save = tk.Button(self.frame3, text="Save Progress", width=15, command=self.save_gene_pool, state="disabled")
        self.save.pack(pady=2)

        self.load = tk.Button(self.frame3, text="Load Progress", width=15, command=self.load_gene_pool, state="normal")
        self.load.pack(pady=2)

        # Ensure thread stops if window is closed
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)


    def save_gene_pool(self):

        with open("gene pool.genesave", "wb") as file:
            pickle.dump((self.gene_pool, self.generation_number, self.best_history, self.truth_table), file)

    def load_gene_pool(self):

        with open("gene pool.genesave", "rb") as file:
            loaded = pickle.load(file)
        self.gene_pool, self.generation_number, self.best_history, self.truth_table = loaded[0], loaded[1], loaded[2], loaded[3]
        self.text_box.insert(tk.END, "Gene pool loaded")
        self.start_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.penalty_button.config(state="normal")
        self.save.config(state="normal")
        self.animate_generation()



    def select_file(self):
        filetypes = (
            ('text files', '*.csv'),
            ('All files', '*.*')
        )


        tt_file = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if len(tt_file) > 0:
            self.truth_table = load_truth_table(tt_file)
            self.best_history = {}

            self.generation_number = 0
            self.gene_pool: list[Species] = prepare_first_generations(self.truth_table, self.generation_number)

            self.open_button.config(text=f"current file: {tt_file}")
            self.start_button.config(state="normal")
            self.stop_button.config(state="normal")
            self.penalty_button.config(state="normal")
            self.save.config(state="normal")

    def animate_generation(self):

        plt.cla()
        for specie in self.best_history:
            gens = []
            score = []
            for generation in self.best_history[specie]:
                gens += [generation]
                score += [self.best_history[specie][generation]]
            self.ax.plot(np.asarray(gens, float), score)

        plt.ylabel('fitness')
        plt.xlabel('generation')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def size_penalty_switch(self):
        if self.size_penalty:
            self.size_penalty = False
            self.penalty_button.config(text="Size Penalty Off")
        else:
            self.size_penalty = True
            self.penalty_button.config(text="Size Penalty On")

    def start_simulation_process(self):
        if self.worker_thread and self.worker_thread.is_alive():
            print("Simulation is already running.")
            return

        print("Starting simulation process...")
        self.running = True
        # Create a NEW thread object each time
        self.worker_thread = threading.Thread(target=self.run, daemon=True)
        self.worker_thread.start()

        # Update button states
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def stop_simulation_process(self):
        if not self.running and (not self.worker_thread or not self.worker_thread.is_alive()):
            print("Simulation is not running.")
            return

        print("Attempting to stop simulation process...")
        self.running = False
        # The thread will check self.running and exit.
        # We don't need to .join() here as it would block the GUI.
        # The daemon=True will handle cleanup if the main app exits.

        # Update button states (could also wait for thread to actually finish
        # by checking is_alive() in a loop with after, but this is simpler for now)
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        print("Stop signal sent. Process will terminate shortly.")


    def run(self):

        # The loop continues as long as self.running is True
        while self.running:

            gene_pool_eval: list[Species] = run_simulation(self.gene_pool, self.truth_table, self.size_penalty)

            best_score = float('inf')
            best_circuit_in_generation = None
            penalty = 1 if self.size_penalty else 0
            self.text_box.delete("1.0", "end")
            self.text_box.insert(tk.END, f"Generation: {self.generation_number}\n\n")
            for score in gene_pool_eval:
                if score.get_best().get_score()[penalty] < best_score:
                    best_score = score.get_best().get_score()[penalty]
                    best_circuit_in_generation = score.get_best()

                if f'{score.get_id()}' not in self.best_history:
                   self.best_history[f'{score.get_id()}'] = {}
                self.best_history[f'{score.get_id()}'][f'{self.generation_number}'] = score.get_best().get_score()[penalty]

                text = f"Fitness: {score.get_best().get_score()[penalty]}\n"
                self.text_box.insert(tk.END, text)

            self.animate_generation() if self.generation_number % 10 == 0 else None

            if self.generation_number % 5 == 0:
                self.text_box_anatomy.delete("1.0", "end")
                self.text_box_anatomy.insert(tk.END, f"{circuit_run_truth_table(best_circuit_in_generation, self.truth_table, debug=True)[1]}\n")

            #new_text = f"Generation: {self.generation_number} fitness score: {list(map(lambda z: z.get_best().get_score()[penalty], gene_pool_eval))}"

            #
            #self.text_box.insert(tk.END, new_text)

            self.gene_pool: list[Species] = prepare_next_generation(gene_pool_eval, self.generation_number, size_penalty=self.size_penalty)
            self.generation_number += 1

        print(f"Simulation loop finished.")

        for x in self.gene_pool:
            print("-------circuit-------")
            x.get_best().visual()
            print("-------circuit-------")
            print("--------test---------")
            circuit_run_truth_table(x.get_best(), self.truth_table, debug=True)
            print("--------test---------")

        # Ensure buttons are correctly set if thread finishes on its own
        # (e.g., if testp had a natural end condition other than self.running)
        # However, for this specific example, stop_test_process handles button states.
        # If the thread could finish for other reasons, you might want to schedule
        # a GUI update from here using master.after:
        # self.master.after(0, self._update_buttons_after_thread_exit)

    # def _update_buttons_after_thread_exit(self):
    #     # This would be called if the thread could end on its own
    #     if not (self.worker_thread and self.worker_thread.is_alive()):
    #         self.start_button.config(state=tk.NORMAL)
    #         self.stop_button.config(state=tk.DISABLED)
    #         print("Thread confirmed exited, buttons updated.")


    def on_closing(self):
        print("Window closing...")
        if self.running and self.worker_thread and self.worker_thread.is_alive():
            self.running = False # Signal thread to stop

            # Optionally, you could wait a very short time for the thread to exit
            #self.worker_thread.join(timeout=2) # Give it half a second
            print("Signalled running thread to stop.")
        plt.close(self.fig)
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1200x800')
    root.title("Logic Gate Evolution")
    app = Gui(root)
    root.mainloop()