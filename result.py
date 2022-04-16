a = 6
b = 10
m = 1950
i = a
while i <= b:
	secondI = 0
	while secondI < i:
		print("*", end="")
		secondI = secondI + 1
	print("\n", end="")
	i = i + 1
i = 1
sum = 0
while a * i < m:
	sum = sum + a * i
	i = i + 1
i = 1
while b * i < m:
	sum = sum + b * i
	i = i + 1
print(sum, end="")
print("\n", end="")
