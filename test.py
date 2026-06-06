import turtle

screen = turtle.Screen()
screen.title("Key Test")

def test():
    print("W PRESSED!")

screen.listen()
screen.onkeypress(test, "w")

screen.mainloop()