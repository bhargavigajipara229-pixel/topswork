number1 = int(input("Enter number 1 "))
number2 = int(input("Enter number 2 "))
ans = number1>100 and number1>number2
print(ans)
ans = number1>100 or number1>number2
print(f"with OR {ans}")
ans=not(number1>100)
