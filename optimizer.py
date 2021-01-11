from optimizer.gate import High, Not, Or, And

if __name__ == "__main__":
    gate = And(Not(High()), High())

    print(f'output of gate {gate.output()}')