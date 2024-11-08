input = "0001 0002"
firstInstruction = input[:4]

match firstInstruction:
    case "0001":
        print("aaa")
    case "0002":
        print("bbb")