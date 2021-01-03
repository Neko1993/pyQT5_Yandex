numbers = input()
sentence = []
word = input()
word = word.split()
numbers = numbers.split()
for i in range(len(numbers)):
    if i == 0:
        word[int(numbers[i])].capitalize()
    else:
        word[int(numbers[i])].lower()
    sentence.append[word[int(numbers[i])]]
for i in sentence:
    print(i, end=' ')
