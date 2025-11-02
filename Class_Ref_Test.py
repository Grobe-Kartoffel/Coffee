class caller:
    sub = None
    def __init__(self):
        self.sub = None
    def call(self):
        self.sub.fcn()
class called:
    msg = ""
    def __init__(self):
        self.msg = "Hello, World!"
    def fcn(self):
        print(self.msg)
def main():
    A = caller()
    B = called()
    A.sub = B
    A.call()
    B.msg = "Goodbye, World!"
    A.call()
    
# -------------------------
main()