def romanConverter(args):
    myromandictones ={"": 0, "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}
    myromandicttens ={"": 0, "X": 10, "XX": 20, "XXX": 30, "XL": 40, "L": 50,
                      "LX": 60, "LXX": 70, "LXXX": 80, "XC": 90, "C": 100}
    myromandicthuns ={"": 0, "C": 100, "CC": 200, "CCC": 300, "CD": 400, "D": 500,
                      "DC": 600, "DCC": 700, "DCCC": 800, "CM": 900, "M": 1000}
    myromandictthous={"": 0, "M": 1000, "MM": 2000, "MMM": 3000}
    # flipping the dictionary using erik's response fron
    # https://stackoverflow.com/questions/1031851/how-do-i-exchange-keys-with-values-in-a-dictionary
    romones = {v: k for k, v in myromandictones.items()}
    romtens = {v: k for k, v in myromandicttens.items()}
    romhuns = {v: k for k, v in myromandicthuns.items()}
    romthous ={v: k for k, v in myromandictthous.items()}

    numericalvalue = 0
    myargs = ""
    if isinstance(args, int):
        thous = args//1000
        args -= (thous * 1000)
        huns = args//100
        args -= (huns * 100)
        tens = args//10
        args -= (tens * 10)
        print("Equivalent roman numeral is:\n")
        print(romthous[thous*1000] + romhuns[huns*100] + romtens[tens*10] + romones[args] + "\n")
   #  elif isinstance(args, str):
   #      myargs = args
   #      myargs = myargs.upper()
   #      if myargs[0] in myromandict:
   #          numericalvalue += myromandict[myargs[0]]
   #          myargs = myargs[1, len(myargs)]
   #      for i in myargs:
   #          if i in myromandict:
   #              numericalvalue += myromandict[i]


romanConverter(int(input("Enter an integer that you're interested in converting to roman numerals! ")))