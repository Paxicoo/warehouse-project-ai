import copy
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import queue
import threading

import constants
from ga.genetic_operators.mutation_swap import MutationSwap
from ga.genetic_operators.mutation_insert import MutationInsert
from ga.genetic_operators.recombination_ox import RecombinationOX
from ga.selection_methods.tournament import Tournament
from ga.genetic_operators.recombination_cx import RecombinationCX
from ga.genetic_operators.recombination_pmx import RecombinationPMX
from ga.genetic_operators.mutation_inversion import MutationInversion
from ga.genetic_algorithm_thread import GeneticAlgorithmThread
from warehouse.warehouse_agent_search import WarehouseAgentSearch, read_state_from_txt_file
from warehouse.warehouse_experiments_factory import WarehouseExperimentsFactory
from warehouse.warehouse_problemforGA import WarehouseProblemGA
from warehouse.warehouse_state import WarehouseState
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch

matplotlib.use("TkAgg")


class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Genetic Algorithms')

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.frame = tk.Frame(master=self)
        self.frame.pack()

        # 0 - OVERALL STRUCTURE ---------------------------------------------

        self.panel_algorithm = tk.PanedWindow(self.frame)
        self.panel_simulation = tk.PanedWindow(self.frame)
        self.panel_algorithm.pack(side='left')
        self.panel_simulation.pack(side='right', fill='both', expand=True)

        self.panel_top = tk.PanedWindow(self.panel_algorithm)
        self.panel_middle = tk.PanedWindow(self.panel_algorithm)
        self.panel_bottom = tk.PanedWindow(self.panel_algorithm)
        self.panel_top.pack()
        self.panel_middle.pack()
        self.panel_bottom.pack()

        # 1 - TOP PANEL -----------------------------------------------------

        self.panel_top_left = tk.PanedWindow(self.panel_top)
        self.panel_top_left.pack(side='left')

        self.panel_top_right = tk.PanedWindow(self.panel_top)
        self.panel_top_right.pack(side='left')

        # 1.1 - Top Left Panel

        self.panel_parameters = tk.PanedWindow(self.panel_top_left)
        self.panel_run = tk.PanedWindow(self.panel_top_left)
        self.panel_parameters.pack()
        self.panel_run.pack()

        # 1.1.1 Parameters Panel

        self.label_seed = tk.Label(master=self.panel_parameters, text="Seed: ", anchor="e", width=25)
        self.label_seed.grid(row=0, column=0)

        self.entry_seed = tk.Entry(master=self.panel_parameters, width=17)
        self.entry_seed.insert(tk.END, '1')
        self.entry_seed.grid(row=0, column=1)

        self.label_population_size = tk.Label(master=self.panel_parameters, text="Population size: ",
                                              anchor="e", width=25)
        self.label_population_size.grid(row=1, column=0)

        self.entry_population_size = tk.Entry(master=self.panel_parameters, width=17)
        self.entry_population_size.insert(tk.END, '100')
        self.entry_population_size.grid(row=1, column=1)

        self.label_num_generations = tk.Label(master=self.panel_parameters, text="# of generations: ",
                                              anchor="e", width=25)
        self.label_num_generations.grid(row=2, column=0)

        self.entry_num_generations = tk.Entry(master=self.panel_parameters, width=17)
        self.entry_num_generations.insert(tk.END, '100')
        self.entry_num_generations.grid(row=2, column=1)

        self.label_selection_methods = tk.Label(master=self.panel_parameters, text="Selection method: ",
                                                anchor="e", width=25)
        self.label_selection_methods.grid(row=3, column=0)

        selection_methods = ['Tournament']

        self.combo_selection_methods = ttk.Combobox(master=self.panel_parameters, state="readonly",
                                                    values=selection_methods, width=14)
        self.combo_selection_methods.set(selection_methods[0])
        self.combo_selection_methods.grid(row=3, column=1)

        self.label_tournament_size = tk.Label(master=self.panel_parameters, text="Tournament size: ",
                                              anchor="e", width=25)
        self.label_tournament_size.grid(row=4, column=0)

        self.entry_tournament_size = tk.Entry(master=self.panel_parameters, width=17)
        self.entry_tournament_size.insert(tk.END, '2')
        self.entry_tournament_size.grid(row=4, column=1)

        self.label_recombination_methods = tk.Label(master=self.panel_parameters, text="Recombination method: ",
                                                    anchor="e", width=25)
        self.label_recombination_methods.grid(row=5, column=0)

        recombination_methods = ['PMX', 'Cycle Crossover', 'Order Crossover']

        self.combo_recombination_methods = ttk.Combobox(master=self.panel_parameters, state="readonly",
                                                        values=recombination_methods, width=14)
        self.combo_recombination_methods.set(recombination_methods[0])
        self.combo_recombination_methods.grid(row=5, column=1)

        self.label_recombination_prob = tk.Label(master=self.panel_parameters, text="Recombination prob.: ",
                                                 anchor="e", width=25)
        self.label_recombination_prob.grid(row=6, column=0)

        self.entry_recombination_prob = tk.Entry(master=self.panel_parameters, width=17)
        self.entry_recombination_prob.insert(tk.END, '0.7')
        self.entry_recombination_prob.grid(row=6, column=1)

        self.label_mutation_methods = tk.Label(master=self.panel_parameters, text="Mutation method: ",
                                               anchor="e", width=25)
        self.label_mutation_methods.grid(row=7, column=0)

        mutation_methods = ['Insert', 'Swap', 'Inversion']

        self.combo_mutation_methods = ttk.Combobox(master=self.panel_parameters, state="readonly",
                                                   values=mutation_methods, width=14)
        self.combo_mutation_methods.set(mutation_methods[0])
        self.combo_mutation_methods.grid(row=7, column=1)

        self.label_mutation_prob = tk.Label(master=self.panel_parameters, text="Mutation prob.: ", anchor="e", width=25)
        self.label_mutation_prob.grid(row=8, column=0)

        self.entry_mutation_prob = tk.Entry(master=self.panel_parameters, width=17)
        self.entry_mutation_prob.insert(tk.END, '0.1')
        self.entry_mutation_prob.grid(row=8, column=1)

        # 1.1.2 Run Panel

        self.button_dataset = tk.Button(master=self.panel_run, text='Problem',
                                        command=self.problem_button_clicked)
        self.button_dataset.pack(side='left', padx=5)

        self.button_runSearch = tk.Button(master=self.panel_run, text='Run Search',
                                          command=self.runSearch_button_clicked)
        self.button_runSearch.pack(side='left', padx=5)

        self.button_runGA = tk.Button(master=self.panel_run, text='Run GA',
                                      command=self.runGA_button_clicked)
        self.button_runGA.pack(side='left', padx=5)

        self.button_stop = tk.Button(master=self.panel_run, text='Stop',
                                     command=self.stop_button_clicked)
        self.button_stop.pack(side='left', padx=5)

        # 2 - MIDDLE PANEL --------------------------------------------------

        self.panel_problem = tk.PanedWindow(self.panel_middle)
        self.panel_problem.pack(side='left', padx=5)

        self.panel_best = tk.PanedWindow(self.panel_middle)
        self.panel_best.pack(side='left', padx=5)

        # 2.1 ProblemPanel

        self.label_problem = tk.Label(master=self.panel_problem, text="Problem data: ", anchor="w", width=46)
        self.label_problem.pack()
        self.text_problem = tk.Text(master=self.panel_problem, state="normal", height=20, width=46)
        self.text_problem.pack()

        # 2.2 Best Panel

        self.label_best = tk.Label(master=self.panel_best, text="Best solution: ", anchor="w", width=46)
        self.label_best.pack()
        self.text_best = tk.Text(master=self.panel_best, state="normal", height=20, width=40)
        self.text_best.pack()

        # 3 - BOTTOM PANEL --------------------------------------------------

        self.button_experiments = tk.Button(master=self.panel_bottom, text='Open experiments',
                                            command=self.open_experiments_button_clicked)
        self.button_experiments.pack(side='left', padx=5)

        self.button_run_experiments = tk.Button(master=self.panel_bottom, text='Run',
                                                command=self.run_experiments_button_clicked)
        self.button_run_experiments.pack(side='left', padx=5)

        self.button_stop_experiments = tk.Button(master=self.panel_bottom, text='Stop',
                                                 command=self.stop_experiments_button_clicked)
        self.button_stop_experiments.pack(side='left', padx=5)

        self.label_status = tk.Label(master=self.panel_bottom, text="status: ")
        self.label_status.pack(side="left", padx=5)

        self.entry_status = tk.Entry(master=self.panel_bottom, width=10)
        self.entry_status.pack(side="left", padx=3)

        # 3 - RIGHT PANEL - Simulation Panel --------------------------------------------------
        self.panel_sim = tk.PanedWindow(self.panel_simulation)

        self.canvas = tk.Canvas(self.panel_sim, bg="white", height=300, width=300)
        self.canvas.pack()

        self.panel_sim.pack(side='top', padx=5)
        self.label_sim = tk.Label(master=self.panel_sim, text="Simulation: ", anchor="w", width=46)
        self.label_sim.pack()

        self.panel_steps_run = tk.PanedWindow(self.panel_simulation)
        self.panel_steps_run.pack(side='bottom', padx=5)

        self.button_simulation = tk.Button(master=self.panel_steps_run, text='Run Simulation',
                                           command=self.sim_button_clicked)
        self.button_simulation.pack(side='left', padx=5)

        self.button_stop_simulation = tk.Button(master=self.panel_steps_run, text='Stop Simulation',
                                                command=self.stop_button_clicked)
        self.button_stop_simulation.pack(side='left', padx=5)

        self.label_steps = tk.Label(master=self.panel_steps_run, text="Steps: ", anchor="w")
        self.label_steps.pack(side="left", padx=5)

        self.text_steps = tk.Entry(master=self.panel_steps_run, width=10)
        self.text_steps.pack(side="left", padx=5)

        # -----------------------------------------------------

        self.Warehouse_problem = None
        self.genetic_algorithm = None
        self.solution_runner = None

        self.generations = None
        self.generation_values = None
        self.average_values = None
        self.best_values = None
        self.line_average_values = None
        self.line_best_values = None
        self.canvas_plot = None
        self.ax = None
        self.after_id = None
        self.queue = queue.Queue()
        self.active_threads = []

        self.draw_empty_plot()

        self.experiments_factory = None
        self.experiments_runner = None

        self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.DISABLED, stop=tk.DISABLED,
                            open_experiments=tk.NORMAL, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                            simulation=tk.DISABLED, stop_simulation=tk.DISABLED)
        # End of constructor -----------------------------------

    def problem_button_clicked(self):
        filename = fd.askopenfilename(initialdir='/data_sets', title='Select a problem')
        if filename:
            matrix, num_rows, num_columns = read_state_from_txt_file(filename)
            self.initial_state = WarehouseState(matrix, num_rows, num_columns)
            self.agent_search = WarehouseAgentSearch(WarehouseState(matrix, num_rows, num_columns))
            self.solution = None
            self.text_problem.delete("1.0", "end")
            self.text_problem.insert(tk.END, str(self.initial_state) + "\n" + str(self.agent_search))
            self.entry_status.delete(0, tk.END)
            self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.NORMAL, runGA=tk.DISABLED, stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                                simulation=tk.DISABLED, stop_simulation=tk.DISABLED)
            rows = self.initial_state.rows
            columns = self.initial_state.columns
            self.canvas.destroy()
            self.canvas = tk.Canvas(self.panel_sim, bg="white", height=16 * (rows + 2), width=16 * (columns + 2))
            self.canvas.pack()
            self.draw_state(self.initial_state)

    def runSearch_button_clicked(self):

        self.agent_search.search_method.stopped = False

        self.text_problem.delete("1.0", "end")

        self.text_problem.insert(tk.END, "Running...\n")

        self.solution = None

        self.manage_buttons(data_set=tk.DISABLED, runSearch=tk.DISABLED, runGA=tk.DISABLED, stop=tk.NORMAL,
                            open_experiments=tk.DISABLED, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                            simulation=tk.DISABLED, stop_simulation=tk.DISABLED)

        self.solver = SearchSolver(self, self.agent_search)
        self.solver.daemon = True
        self.solver.start()

    def runGA_button_clicked(self):

        if self.problem_ga is None:
            messagebox.showwarning("Warning", "You should define a problem first (Problem button)")
            return

        if not self.validate_parameters():
            return

        selection_method = Tournament(int(self.entry_tournament_size.get()))
        recombination_methods_index = self.combo_recombination_methods.current()
        recombination_method = RecombinationPMX(
            float(self.entry_recombination_prob.get())) if recombination_methods_index == 0 else \
            RecombinationCX(float(self.entry_recombination_prob.get())) if recombination_methods_index == 1 else \
                RecombinationOX(float(self.entry_recombination_prob.get()))

        mutation_methods_index = self.combo_mutation_methods.current()
        mutation_method = MutationInversion(
            float(self.entry_mutation_prob.get())) if mutation_methods_index == 0 else \
            MutationSwap(float(self.entry_mutation_prob.get())) if mutation_methods_index == 1 else \
                MutationInsert(float(self.entry_mutation_prob.get()))

        self.genetic_algorithm = GeneticAlgorithmThread(
            int(self.entry_seed.get()),
            int(self.entry_population_size.get()),
            int(self.entry_num_generations.get()),
            selection_method,
            recombination_method,
            mutation_method
        )

        self.queue.queue.clear()
        self.generations = 0
        self.generation_values = []
        self.average_values = []
        self.best_values = []

        self.genetic_algorithm.problem = self.problem_ga
        self.genetic_algorithm.add_tkinter_listener(self)
        self.genetic_algorithm.daemon = True
        self.genetic_algorithm.start()
        self.update_idletasks()
        self.after_id = self.after(0, self.generation_ended)
        self.manage_buttons(data_set=tk.DISABLED, runSearch=tk.DISABLED, runGA=tk.DISABLED, stop=tk.NORMAL,
                            open_experiments=tk.DISABLED, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                            simulation=tk.NORMAL, stop_simulation=tk.DISABLED)
        self.entry_status.delete(0, tk.END)

    def sim_button_clicked(self):

        self.manage_buttons(data_set=tk.DISABLED, runSearch=tk.DISABLED, runGA=tk.DISABLED, stop=tk.DISABLED,
                            open_experiments=tk.DISABLED, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                            simulation=tk.DISABLED, stop_simulation=tk.NORMAL)
        self.queue.queue.clear()
        best_in_run = self.genetic_algorithm.best_in_run
        self.solution_runner = SolutionRunner(self, best_in_run, copy.deepcopy(self.initial_state))
        self.solution_runner.daemon = True
        self.solution_runner.start()
        self.active_threads.append(self.solution_runner)
        self.update_idletasks()
        self.after_id = self.after(0, self.show_solution_step)

    def show_solution_step(self):
        if not self.queue.empty():
            state, step, done = self.queue.get()
            if done:
                self.queue.queue.clear()
                self.after_cancel(self.after_id)
                self.after_id = None
                self.solution_runner = None
                self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                    open_experiments=tk.NORMAL, run_experiments=tk.DISABLED,
                                    stop_experiments=tk.DISABLED,
                                    simulation=tk.NORMAL, stop_simulation=tk.DISABLED)
                return
            self.draw_state(state)
            self.text_steps.delete("0", "end")
            self.text_steps.insert(tk.END, step + 1)
        self.update_idletasks()
        self.after_id = self.after(100, self.show_solution_step)

    def draw_state(self, state):
        rows = state.rows
        columns = state.columns
        i = 0

        for row in range(rows):
            for col in range(columns):
                x1 = (col + 1) * 16
                y1 = (row + 1) * 16
                x2 = x1 + 16
                y2 = y1 + 16
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=state.get_cell_color(row, col))

                if state.matrix[row][col] == constants.PRODUCT or state.matrix[row][col] == constants.PRODUCT_CATCH:
                    i += 1
                    self.canvas.create_text(x1 + 8, y1 + 8, text=str(i), font=("Arial", 9))

    def stop_button_clicked(self):
        if self.solver is not None and not self.solver.agent.search_method.stopped:
            self.solver.stop()
            self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.NORMAL, runGA=tk.DISABLED, stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                                simulation=tk.DISABLED, stop_simulation=tk.DISABLED)
            self.solver = None
            return

        if self.solution_runner is not None and self.solution_runner.thread_running:
            self.solution_runner.stop()
            self.queue.queue.clear()
            self.after_cancel(self.after_id)
            self.after_id = None
            self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                                simulation=tk.NORMAL, stop_simulation=tk.DISABLED)
            self.solution_runner = None
            return

        if self.genetic_algorithm is not None:
            self.genetic_algorithm.stop()
            self.queue.queue.clear()
            self.after_cancel(self.after_id)
            self.after_id = None
            self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                                simulation=tk.DISABLED, stop_simulation=tk.DISABLED)
            self.genetic_algorithm = None

    def open_experiments_button_clicked(self):
        filename = fd.askopenfilename(initialdir='.')
        if filename:
            self.experiments_factory = WarehouseExperimentsFactory(filename)
            self.manage_buttons(data_set=self.button_dataset['state'],
                                runSearch=tk.DISABLED, runGA=self.button_runGA['state'], stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.NORMAL, stop_experiments=tk.DISABLED,
                                simulation=tk.DISABLED, stop_simulation=tk.DISABLED)

    def run_experiments_button_clicked(self):
        self.experiments_runner = ExperimentsRunner(self)
        self.experiments_runner.daemon = True
        self.experiments_runner.start()
        self.manage_buttons(data_set=tk.DISABLED, runSearch=tk.DISABLED, runGA=tk.DISABLED, stop=tk.DISABLED,
                            open_experiments=tk.DISABLED, run_experiments=tk.DISABLED, stop_experiments=tk.NORMAL,
                            simulation=tk.DISABLED, stop_simulation=tk.DISABLED)
        self.entry_status.delete(0, tk.END)
        self.entry_status.insert(tk.END, 'Running')

    def stop_experiments_button_clicked(self):
        if self.experiments_runner is not None:
            self.experiments_runner.stop()
        self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.DISABLED, stop=tk.DISABLED,
                            open_experiments=tk.NORMAL, run_experiments=tk.NORMAL, stop_experiments=tk.DISABLED,
                            simulation=tk.DISABLED, stop_simulation=tk.DISABLED)

    def on_closing(self):
        if self.genetic_algorithm:
            self.genetic_algorithm.stop()
        if self.experiments_runner:
            self.experiments_runner.stop()
        self.destroy()

    def manage_buttons(self, data_set, runSearch, runGA, stop, open_experiments, run_experiments, stop_experiments,
                       simulation, stop_simulation):
        self.button_dataset['state'] = data_set
        self.button_runSearch['state'] = runSearch
        self.button_runGA['state'] = runGA
        self.button_stop['state'] = stop
        self.button_experiments['state'] = open_experiments
        self.button_run_experiments['state'] = run_experiments
        self.button_stop_experiments['state'] = stop_experiments
        self.button_simulation['state'] = simulation
        self.button_stop_simulation['state'] = stop_simulation

    def generation_ended(self):
        if not self.queue.empty():
            ga_info = self.queue.get()
            if ga_info.run_ended:
                self.queue.queue.clear()
                self.after_cancel(self.after_id)
                self.after_id = None
                self.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                    open_experiments=tk.NORMAL, run_experiments=tk.DISABLED,
                                    stop_experiments=tk.DISABLED, simulation=tk.NORMAL, stop_simulation=tk.DISABLED)
                return
            self.text_best.delete("1.0", "end")
            self.text_best.insert(tk.END, str(ga_info.best))
            self.generation_values.append(self.generations)
            self.average_values.append(ga_info.average_fitness)
            self.best_values.append(ga_info.best.fitness)
            self.generations += 1
            self.update_plot()
        self.update_idletasks()
        self.after_id = self.after(0, self.generation_ended)

    def draw_empty_plot(self):
        fig = Figure(figsize=(5, 2.5), dpi=100)
        self.ax = fig.add_subplot(111)
        self.line_average_values, = self.ax.plot([], [], label='Average')
        self.line_best_values, = self.ax.plot([], [], label='Best')
        self.ax.legend()
        self.canvas_plot = FigureCanvasTkAgg(fig, master=self.panel_top_right)
        self.canvas_plot.draw()
        self.canvas_plot.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

    def update_plot(self):
        self.line_average_values.set_data(self.generation_values, self.average_values)
        self.line_best_values.set_data(self.generation_values, self.best_values)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas_plot.draw()

    def validate_parameters(self) -> bool:
        try:
            seed = int(self.entry_seed.get())
            if seed <= 0:
                messagebox.showwarning("Warning", "Seed should be a positive integer")
                return False
        except ValueError:
            messagebox.showwarning("Warning", "Seed should be a positive integer")
            return False

        try:
            population_size = int(self.entry_population_size.get())
            if population_size <= 1 or population_size % 2 != 0:
                messagebox.showwarning("Warning", "Population size should be an even positive integer")
                return False
        except ValueError:
            messagebox.showwarning("Warning", "Population size should be an even positive integer")
            return False

        try:
            num_generations = int(self.entry_num_generations.get())
            if num_generations <= 0:
                messagebox.showwarning("Warning", "Number of generations should be a positive integer")
                return False
        except ValueError:
            messagebox.showwarning("Warning", "Number of generations should be a positive integer")
            return False

        if self.combo_selection_methods.current() == 0:
            try:
                tournament_size = int(self.entry_tournament_size.get())
                if tournament_size < 2 or tournament_size > population_size - 1:
                    messagebox.showwarning("Warning", "Tournament size should be a positive integer larger than 1"
                                                      " and smaller than the population size")
                    return False
            except ValueError:
                messagebox.showwarning("Warning", "Tournament size should be a positive integer larger than 1"
                                                  " and smaller than the population size")
                return False

        try:
            recombination_prob = float(self.entry_recombination_prob.get())
            if recombination_prob < 0 or recombination_prob > 1:
                messagebox.showwarning("Warning", "Recombination probability should be a float in [0, 1]")
                return False
        except ValueError:
            messagebox.showwarning("Warning", "Recombination probability should be a float in [0, 1]")
            return False

        try:
            mutation_prob = float(self.entry_mutation_prob.get())
            if mutation_prob < 0 or mutation_prob > 1:
                messagebox.showwarning("Warning", "Mutation probability should be a float in [0, 1]")
                return False
        except ValueError:
            messagebox.showwarning("Warning", "Mutation probability should be a float in [0, 1]")
            return False

        return True


class ExperimentsRunner(threading.Thread):

    def __init__(self, gui: Window):
        super(ExperimentsRunner, self).__init__()
        self.gui = gui
        self.experiments_factory = gui.experiments_factory
        self.thread_running = False

    def stop(self):
        self.thread_running = False
        self.gui.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.NORMAL,
                                stop_experiments=tk.DISABLED, simulation=tk.DISABLED, stop_simulation=tk.DISABLED)

    def run(self):
        self.thread_running = True

        while self.experiments_factory.has_more_experiments() and self.thread_running:
            experiment = self.experiments_factory.next_experiment()
            experiment.run()

        self.gui.text_best.insert(tk.END, '')
        if self.thread_running:
            self.gui.entry_status.delete(0, tk.END)
            self.gui.entry_status.insert(tk.END, 'Done')
            self.gui.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                    open_experiments=tk.NORMAL, run_experiments=tk.DISABLED,
                                    stop_experiments=tk.DISABLED, simulation=tk.DISABLED, stop_simulation=tk.DISABLED)


class SearchSolver(threading.Thread):

    def __init__(self, gui: Window, agent: WarehouseAgentSearch):
        super(SearchSolver, self).__init__()
        self.gui = gui
        self.agent = agent

    def stop(self):
        self.agent.stop()

    def run(self):
        # calcular os pares

        # para cada par, definir
        # criar uma instancia da classe problemForSearch
        # enviar no initialState o agente e o goal corretamente iniciados
        # Problem(intiailState, goal_position (a maior parte das vezes e a celula 2 se for porta)
        # se for produto é cell 2 + 1 ou cell 2 - 1 (depende do sitio do produto)

        # par tem a Cell1 e Cell2, o initial State tem o agente na Cell 1, o goal é a Cell 2 (se for a porta)

        # cada par tem um goal diferente, e vai ter um estado inicial diferente

        # tambem tenho a distancia a porta (isso e em cima da porta)

        # primeiro vamos tentar resolver UM PAR
        # p = agent.pairs[0] --> primeiro par, corresponde do agente ao primeiro produto
        # primeiro par é 4-4 / 1-4 cell1.linha = 4 , cell1.coluna = 4, cell2.linha = 1, cell2.coluna = 4
        # o agente ja tem o initial environment (é um state)

        # posicionar o agente na celula1 (cell1) !!!!
        # posicionar a forklift na cell1

        # problem = warehouseProblemSearch (initialenvironment, goalposition)

        # o goalposition não é o produto em si, mas sim a célula ao lado (esquerda ou direita)
        # verificar na matriz do initial environment, se ao lado esquerdo do produto está vazio,
        # se não estiver, então o agente tem que estar no lado direito

        # se verificarmos que a celula 1 é um agente, vamos posicionar lá o agente

        # se o goal_position for uma porta, é direto... se for um produto o goal_position é +1 ou -1 do produto

        # solution = agent.solve_problem(problem) --> o problem já foi definido, é o goal

        # p (pair) p.value = s.cost (s de solution)

        # temos de fazer um for para percorrer todos os pares (calcular o custo) e fazer genérico
        # ou seja, depende se goal é porta ou produto

        # vamos agora recapitular o que é preciso para calcular um par (só depois disso calcula-se os outros pares)

        # neste nesta classe recebemos o agente, entao podemos logo fazer
        # p = self.agent.pairs[0] --> primeiro par, se funcionar fazemos um ciclo for para todos os pares

        # depois de buscar o par, vamos buscar a celula 1 do par
        # cell1 = Cell (copy of p.cell1) --> fazer import

        # agora vamos buscar a celula 2
        # cell2 = Cell (copy of p.cell2)

        # se fosse do agente à porta era muito simples, bastava fazer isto
        # self.agent.initial_environment.line_forklift=cell1.line
        # self.agent.initial_environment.column_forklift=cell1.column

        # faz se uma copia para nao alterar o ambiente inicial
        # state = copy of self.agent.initial_environment

        # tem que se alterar as coordenadas da cell1 se for diferente de um agent
        # (se for produto, cell1 é esquerda ou direita, o que tiver livre ao lado do produto)

        # agora vamos definir o problema
        # problem = WarehouseProblemSearch(state, cell2)
        # nao esquecendo que temos de alterar as coordenadas da cell2 se for diferente da porta

        # agora fazemos
        # solution = self.agent.solve_problem(problem)

        # no final
        # (p de pair) p.value = solution.cost

        # depois deve tar num ciclo para fazer com todos os pares

        # depois mostrar os dados na parte gráfica, tens que se ir a
        # self.text_problem.insert(tk.END, self.agent);
        # ver as linhas 273 (nao mostrar o state, apenas o agente)

        # depois de resolver todos os pares, temos de fazer o GA

        # Iterar por todos os pares
        for pair in self.agent.pairs:
            # Fazer uma cópia das células do par
            cell1 = copy.copy(pair.cell1)
            cell2 = copy.copy(pair.cell2)

            # Atualizar o estado inicial com a posição da forklift na cell1
            state = copy.copy(self.agent.initial_environment)

            # Verificar se a cell1 é um produto, e ajustar a posição do agente se necessário
            cell1_content = state.matrix[cell1.line][cell1.column]
            if cell1_content == 2:
                if cell1.column != 0 and state.matrix[cell1.line][cell1.column - 1] == 0:
                    state.line_forklift = cell1.line
                    state.column_forklift = cell1.column - 1
                else:
                    state.line_forklift = cell1.line
                    state.column_forklift = cell1.column + 1
            else:
                state.line_forklift = cell1.line
                state.column_forklift = cell1.column

            # Verificar se o goal é um produto, e ajustar a posição da cell2 se necessário
            cell2_content = state.matrix[cell2.line][cell2.column]
            if cell2_content == 2:
                if cell2.column != 0 and state.matrix[cell2.line][cell2.column - 1] == 0:
                    cell2.column -= 1
                else:
                    cell2.column += 1

            # Criar uma instância da classe WarehouseProblemSearch com o estado inicial atualizado e a posição da porta
            problem = WarehouseProblemSearch(state, cell2)

            # Resolver o problema
            solution = self.agent.solve_problem(problem)

            # Atualizar a distância do par
            pair.value = solution.cost

            # Adicionar a distância ao dicionário de distâncias usando as coordenadas das células
            self.agent.distances[
                ((pair.cell1.line, pair.cell1.column), (pair.cell2.line, pair.cell2.column))] = solution.cost

            self.agent.paths[(
            (pair.cell1.line, pair.cell1.column), (pair.cell2.line, pair.cell2.column))] = solution.obtain_all_path()

            pair.solution = solution

            # Imprimir a distância para debugging
            #print(f"Distance for pair {pair}")

        self.agent.search_method.stopped = True
        self.gui.text_problem.delete("1.0", "end")
        self.gui.text_problem.insert(tk.END, "\n" + str(self.agent))
        self.gui.problem_ga = WarehouseProblemGA(self.agent)
        self.gui.manage_buttons(data_set=tk.NORMAL, runSearch=tk.DISABLED, runGA=tk.NORMAL, stop=tk.DISABLED,
                                open_experiments=tk.NORMAL, run_experiments=tk.DISABLED, stop_experiments=tk.DISABLED,
                                simulation=tk.DISABLED, stop_simulation=tk.DISABLED)


class SolutionRunner(threading.Thread):

    def __init__(self, gui: Window, best_in_run, state: WarehouseState):
        super(SolutionRunner, self).__init__()
        self.gui = gui
        self.best_in_run = best_in_run
        self.state = state
        self.thread_running = False

    def stop(self):
        self.thread_running = False

    def run(self):
        self.thread_running = True
        self.state.line_exit = self.best_in_run.problem.agent_search.exit.line
        self.state.column_exit = self.best_in_run.problem.agent_search.exit.column
        forklift_path, steps = self.best_in_run.obtain_all_path()
        old_cell = [None] * len(forklift_path)
        new_cells = []
        for step in range(steps - 1):
            new_cells.clear()
            if not self.thread_running:
                return
            for j in range(len(forklift_path)):
                if old_cell[j] is None:
                    firs_cell = forklift_path[j][0]
                    old_cell[j] = firs_cell
                if step < len(forklift_path[j]) - 1:
                    if old_cell[j] not in new_cells:
                        self.state.matrix[old_cell[j].line][old_cell[j].column] = constants.EMPTY
                    new_cell = forklift_path[j][step + 1]
                    new_cells.append(new_cell)
                    self.state.matrix[new_cell.line][new_cell.column] = constants.FORKLIFT
                    old_cell[j] = new_cell
                else:
                    self.state.matrix[old_cell[j].line][old_cell[j].column] = constants.FORKLIFT

                # TODO put the catched products in black
                # basicamente, contabilizar em que step é que ele apanha cada um dos produtos
                # se tivesse nesse step, ficava a preto
            self.gui.queue.put((copy.deepcopy(self.state), step, False))
        self.gui.queue.put((None, steps, True))  # Done
