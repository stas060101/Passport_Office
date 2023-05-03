class Person:
    def __init__(self, name, father=None, mother=None):
        self.name = name
        self.father = father
        self.mother = mother

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_parents(self):
        return self.father, self.mother


def print_family_tree(person, level=0):
    print(" - " * level + str(person))
    father, mother = person.get_parents()
    if father:
        print_family_tree(father, level + 1)
    if mother:
        print_family_tree(mother, level + 1)


# батьки діда_1
grand_grandfather1 = Person("прадід діда по баті")
grand_grandmother1 = Person("прабаба діда по баті")

# батьки баби_1
grand_grandfather2 = Person("прадід баби по баті")
grand_grandmother2 = Person("прабаба баби по баті")

# батьки діда_2
grand_grandfather3 = Person("прадід діда по матері")
grand_grandmother3 = Person("прабаба діда по матері")

# батьки баби_2
grand_grandfather4 = Person("прадід баби по матері")
grand_grandmother4 = Person("прабаба баби по матері")

# батьки баті
grandfather1 = Person("дід по баті", father=grand_grandfather1, mother=grand_grandmother1)
grandmother1 = Person("баба по баті", father=grand_grandfather2, mother=grand_grandmother2)

# батьки мати
grandfather2 = Person("дід по матері", father=grand_grandfather3, mother=grand_grandmother3)
grandmother2 = Person("баба по матері", father=grand_grandfather4, mother=grand_grandmother4)

father = Person("батько", father=grandfather1, mother=grandmother1)
mother = Person("мати", father=grandfather2, mother=grandmother2)
son = Person("син", father=father, mother=mother)

print_family_tree(son)
