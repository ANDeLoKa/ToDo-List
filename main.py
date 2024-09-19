from GUI import GUI

# exit const codes
EXIT_SUCCESSFUL = 0
EXIT_FAILURE = -1

if (__name__ == "__main__"):

    App = GUI()
    App.mainloop()

    exit(EXIT_SUCCESSFUL)