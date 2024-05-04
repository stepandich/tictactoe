"""
Модуль игры крестики/нолики в графическом окне.
Используется библиотека  tkinter для построения графического интерфейса приложения.
Будут использоваться кнопки для отображения ячеек и управления ими.


"""
import tkinter as tk


def create_grid(frame_m, event=None):
    # Clear any previous widgets
    for widget in frame_m.winfo_children():
        widget.destroy()

    for i in range(3):
        for j in range(3):
            frame = tk.Button(
                master=frame_m,
                relief=tk.RAISED,
                borderwidth=1,
                text=f"Row {i}\nColumn {j}"
            )
            frame.grid(row=i, column=j, sticky="nsew")
            # label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
            # label.grid(row=i, column=j)
            # label.pack()


window = tk.Tk(screenName="test", className="cls")

window.title("tic-toe")
window.geometry("500x500")  # set starting size of window
window.maxsize(500, 500)  # width x height

main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True)
main_frame.bind("<Configure>", create_grid(main_frame))

window.mainloop()
