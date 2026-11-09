# Jogo educativo de lógica proposicional feito com Python + Tkinter.
# Não precisa instalar bibliotecas externas.

BG = "#101827"
PANEL = "#1b2940"
CYAN = "#42d9e8"
WHITE = "#f2f6ff"
MUTED = "#aab8cc"
GREEN = "#5ee0a0"
RED = "#ff7185"
GOLD = "#ffd166"

QUESTIONS = [
    ("Se p=True e q=False, qual é o valor de p ∧ q?", ["Verdadeiro", "Falso"], 1,
     "A conjunção só é verdadeira quando as duas proposições são verdadeiras."),
    ("Se p=True e q=False, qual é o valor de p ∨ q?", ["Verdadeiro", "Falso"], 0,
     "A disjunção é verdadeira quando pelo menos uma proposição é verdadeira."),
    ("Se p=True, qual é o valor de ¬p?", ["Verdadeiro", "Falso"], 1,
     "A negação inverte o valor lógico: ¬V = F."),
    ("Se p=True e q=False, qual é o valor de p → q?", ["Verdadeiro", "Falso"], 1,
     "A condicional só é falsa quando p é verdadeira e q é falsa."),
    ("Se p=True e q=True, qual é o valor de p ↔ q?", ["Verdadeiro", "Falso"], 0,
     "O bicondicional é verdadeiro quando os dois lados têm o mesmo valor."),
    ("Se p=False e q=False, qual é o valor de p ∨ q?", ["Verdadeiro", "Falso"], 1,
     "A disjunção é falsa quando as duas proposições são falsas."),
    ("Se p=False e q=True, qual é o valor de p → q?", ["Verdadeiro", "Falso"], 0,
     "Uma condicional com antecedente falso é considerada verdadeira."),
    ("Se p=True e q=True, qual é o valor de ¬p ∨ q?", ["Verdadeiro", "Falso"], 0,
     "¬p é falso; falso OU verdadeiro resulta em verdadeiro."),
    ("Se p=True e q=False, qual é o valor de (p ∧ ¬q)?", ["Verdadeiro", "Falso"], 0,
     "¬q é verdadeiro; verdadeiro E verdadeiro resulta em verdadeiro."),
    ("Se p=False e q=True, qual é o valor de p ↔ q?", ["Verdadeiro", "Falso"], 1,
     "O bicondicional é falso quando os valores são diferentes.")
]

class EnigmaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Enigma — A Prisão Lógica")
        self.root.geometry("920x650")
        self.root.configure(bg=BG)
        self.root.minsize(760, 560)
        self.players = []
        self.turn = 0
        self.position = 0
        self.current_question = None
        self.game_over = False
        self.build_start()

    def label(self, parent, text, size=12, color=WHITE, bold=False, **kwargs):
        return tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color,
                        font=("Arial", size, "bold" if bold else "normal"),
                        wraplength=kwargs.get("wraplength", 760), justify="center")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_start(self):
        self.clear()
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True, fill="both", padx=35, pady=30)
        self.label(frame, "ENIGMA", 34, CYAN, True).pack(pady=(35, 4))
        self.label(frame, "A PRISÃO LÓGICA", 18, WHITE, True).pack()
        self.label(frame, "Resolva os desafios de lógica proposicional, conquiste chaves\n"
                          "e encontre a saída antes que suas vidas acabem.", 13, MUTED).pack(pady=22)
        card = tk.Frame(frame, bg=PANEL, padx=25, pady=22)
        card.pack(pady=10)
        self.label(card, "Quantos jogadores vão participar?", 14, WHITE, True).pack(pady=(0, 12))
        self.count_var = tk.IntVar(value=2)
        options = tk.Frame(card, bg=PANEL)
        options.pack()
        for n in range(2, 6):
            tk.Radiobutton(options, text=str(n), variable=self.count_var, value=n,
                           bg=PANEL, fg=WHITE, selectcolor=BG, activebackground=PANEL,
                           activeforeground=CYAN, font=("Arial", 12)).pack(side="left", padx=12)
        tk.Button(frame, text="COMEÇAR JOGO", command=self.setup_players,
                  bg=CYAN, fg=BG, activebackground="#8af2f7", relief="flat",
                  font=("Arial", 12, "bold"), padx=25, pady=12, cursor="hand2").pack(pady=22)
        self.label(frame, "Como jogar: lance o dado, avance pelo corredor e responda aos desafios.\n"
                          "Cada resposta correta concede uma chave. Você precisa de 2 chaves\n"
                          "para abrir a porta final. Uma resposta errada custa uma vida.", 10, MUTED).pack(pady=8)

    def setup_players(self):
        count = self.count_var.get()
        self.players = []
        for i in range(count):
            name = simpledialog.askstring("Jogador", f"Nome do jogador {i+1}:", parent=self.root)
            if not name or not name.strip():
                name = f"Jogador {i+1}"
            self.players.append({"name": name.strip(), "lives": 3, "keys": 0, "pos": 0})
        self.turn = 0
        self.game_over = False
        self.build_board()

    def build_board(self):
        self.clear()
        outer = tk.Frame(self.root, bg=BG, padx=24, pady=18)
        outer.pack(fill="both", expand=True)
        self.label(outer, "ENIGMA — A PRISÃO LÓGICA", 22, CYAN, True).pack(pady=(0, 12))
        self.status = tk.Label(outer, text="", bg=PANEL, fg=WHITE,
                              font=("Arial", 11), padx=12, pady=12)
        self.status.pack(fill="x", pady=5)

        board = tk.Frame(outer, bg=BG)
        board.pack(pady=20)
        self.cells = []
        names = ["ENTRADA", "∧", "CORREDOR", "∨", "¬", "PORTA 1",
                 "→", "CORREDOR", "↔", "∧", "PORTA 2", "∨",
                 "¬", "DESAFIO FINAL", "SAÍDA"]
        for i, name in enumerate(names):
            cell = tk.Frame(board, bg=PANEL, width=150, height=75,
                            highlightbackground="#334761", highlightthickness=1)
            cell.grid(row=i // 5, column=i % 5, padx=5, pady=5)
            cell.pack_propagate(False)
            tk.Label(cell, text=f"{i+1}. {name}", bg=PANEL, fg=CYAN if i in (5,10,13,14) else WHITE,
                     font=("Arial", 10, "bold"), wraplength=130).pack(expand=True)
            self.cells.append(cell)

        self.players_display = tk.Label(outer, text="", bg=BG, fg=MUTED,
                                        font=("Arial", 10), justify="left")
        self.players_display.pack(pady=5)
        controls = tk.Frame(outer, bg=BG)
        controls.pack(pady=12)
        self.roll_button = tk.Button(controls, text="🎲 LANÇAR DADO", command=self.roll,
                                     bg=CYAN, fg=BG, relief="flat",
                                     font=("Arial", 12, "bold"), padx=20, pady=10)
        self.roll_button.pack(side="left", padx=8)
        tk.Button(controls, text="REGRAS", command=self.show_rules, bg=PANEL,
                  fg=WHITE, relief="flat", padx=18, pady=10).pack(side="left", padx=8)
        self.refresh()

    def refresh(self):
        if not hasattr(self, "status"):
            return
        p = self.players[self.turn]
        self.status.config(text=f"Vez de {p['name']}   |   Vidas: {p['lives']}   |   Chaves: {p['keys']}")
        lines = []
        for player in self.players:
            lines.append(f"{player['name']}: casa {player['pos']+1}/15  •  vidas: {player['lives']}  •  chaves: {player['keys']}")
        self.players_display.config(text="\n".join(lines))
        for i, cell in enumerate(self.cells):
            occupants = [x["name"] for x in self.players if x["pos"] == i and x["lives"] > 0]
            cell.config(bg="#24445a" if occupants else PANEL)
            for child in cell.winfo_children():
                child.config(bg="#24445a" if occupants else PANEL)
            if occupants:
                child = tk.Label(cell, text=" / ".join(occupants), bg="#24445a",
                                 fg=GOLD, font=("Arial", 8, "bold"), wraplength=130)
                child.pack(side="bottom", pady=2)

    def roll(self):
        if self.game_over:
            return
        p = self.players[self.turn]
        if p["lives"] <= 0:
            self.next_turn()
            return
        dice = random.randint(1, 3)
        p["pos"] = min(14, p["pos"] + dice)
        messagebox.showinfo("Dado", f"{p['name']} tirou {dice} e avançou para a casa {p['pos']+1}.")
        self.refresh()
        self.resolve_tile()

    def resolve_tile(self):
        p = self.players[self.turn]
        pos = p["pos"]
        if pos == 5 and p["keys"] < 1:
            messagebox.showwarning("Porta bloqueada", "Você precisa de pelo menos 1 chave para passar. Volte uma casa.")
            p["pos"] = 4
            self.refresh()
            self.next_turn()
        elif pos == 10 and p["keys"] < 2:
            messagebox.showwarning("Porta bloqueada", "Você precisa de 2 chaves para passar. Volte uma casa.")
            p["pos"] = 9
            self.refresh()
            self.next_turn()
        elif pos == 14:
            self.final_challenge()
        elif pos in (1, 3, 4, 6, 8, 9, 11, 12, 13):
            self.ask_question()
        else:
            self.next_turn()

    def ask_question(self, final=False):
        self.current_question = random.choice(QUESTIONS)
        question, options, answer, explanation = self.current_question
        win = tk.Toplevel(self.root)
        win.title("Desafio de lógica")
        win.configure(bg=BG)
        win.geometry("560x330")
        win.transient(self.root)
        win.grab_set()
        self.label(win, "DESAFIO DE LÓGICA", 18, CYAN, True).pack(pady=(22, 12), padx=20)
        self.label(win, question, 14, WHITE, True, wraplength=500).pack(pady=12, padx=20)
        choice = tk.IntVar(value=-1)
        for i, option in enumerate(options):
            tk.Radiobutton(win, text=option, variable=choice, value=i, bg=BG, fg=WHITE,
                           selectcolor=PANEL, activebackground=BG, font=("Arial", 12)).pack(pady=5)
        def submit():
            if choice.get() not in (0, 1):
                messagebox.showwarning("Atenção", "Escolha uma resposta.", parent=win)
                return
            win.destroy()
            p = self.players[self.turn]
            if choice.get() == answer:
                p["keys"] += 1
                messagebox.showinfo("Correto!", "Você ganhou uma chave!\n\n" + explanation)
            else:
                p["lives"] -= 1
                messagebox.showerror("Resposta incorreta", "Você perdeu uma vida.\n\n" + explanation)
            self.refresh()
            if final:
                if choice.get() == answer and p["keys"] >= 2:
                    self.finish(p)
                else:
                    if p["lives"] <= 0:
                        messagebox.showinfo("Fim de jogo", f"{p['name']} ficou sem vidas.")
                    self.next_turn()
            else:
                if p["lives"] <= 0:
                    messagebox.showinfo("Eliminado", f"{p['name']} ficou sem vidas.")
                self.next_turn()
        tk.Button(win, text="CONFIRMAR", command=submit, bg=CYAN, fg=BG,
                  relief="flat", font=("Arial", 11, "bold"), padx=20, pady=8).pack(pady=18)

    def final_challenge(self):
        p = self.players[self.turn]
        if p["keys"] < 2:
            messagebox.showwarning("Desafio final", "Você precisa de 2 chaves para tentar abrir a saída.")
            p["pos"] = 12
            self.refresh()
            self.next_turn()
            return
        self.ask_question(final=True)

    def next_turn(self):
        if self.game_over:
            return
        alive = [i for i, p in enumerate(self.players) if p["lives"] > 0]
        if not alive:
            self.game_over = True
            messagebox.showinfo("Fim de jogo", "Todos os jogadores perderam suas vidas. A prisão venceu!")
            self.build_start()
            return
        for _ in range(len(self.players)):
            self.turn = (self.turn + 1) % len(self.players)
            if self.players[self.turn]["lives"] > 0:
                break
        self.refresh()

    def finish(self, player):
        self.game_over = True
        messagebox.showinfo("VOCÊ ESCAPOU!", f"Parabéns, {player['name']}!\nVocê resolveu o desafio final e escapou da Prisão Lógica.")
        if messagebox.askyesno("Jogar novamente", "Deseja iniciar uma nova partida?"):
            self.build_start()
        else:
            self.root.destroy()

    def show_rules(self):
        messagebox.showinfo("Regras", "1. Cada jogador começa com 3 vidas.\n"
            "2. Na sua vez, lance o dado e avance de 1 a 3 casas.\n"
            "3. Casas com símbolos apresentam desafios proposicionais.\n"
            "4. Resposta correta: ganha 1 chave. Resposta errada: perde 1 vida.\n"
            "5. A primeira porta exige 1 chave; a segunda exige 2.\n"
            "6. Para escapar, alcance a saída com 2 chaves e acerte o desafio final.\n\n"
            "Conectivos: ∧ (E), ∨ (OU), ¬ (NÃO), → (SE...ENTÃO), ↔ (SE E SOMENTE SE).")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnigmaGame(root)
    root.mainloop()
