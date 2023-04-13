from passport_office import db


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.name = kwargs.get('last_name')
        self.name = kwargs.get('middle_name')
        self.name = kwargs.get('date_of_birth')
        self.name = kwargs.get('sex')

    # marriage = db.relationship('Marriage', lazy=True)
    death = db.relationship('Death', backref='person')
    sex_change = db.relationship('SexChange', backref='person')
    # birth = db.relationship('Birth', backref='person')
    # adoption = db.relationship('Adoption', backref='person')
    history = db.relationship('History', backref='person')
    # genealogy = db.relationship('Genealogy', backref='person')


class Marriage(db.Model):
    __tablename__ = "marriage"

    id = db.Column(db.Integer, primary_key=True)
    husband_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    wife_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date_of_marriage = db.Column(db.DateTime, nullable=False)

    husband = db.relationship('Person', foreign_keys="Marriage.husband_id")
    wife = db.relationship('Person', foreign_keys="Marriage.wife_id")

    divorce = db.relationship('Divorce', backref='marriage')


class Divorce(db.Model):
    __tablename__ = "divorce"

    id = db.Column(db.Integer, primary_key=True)
    marriage_id = db.Column(db.Integer, db.ForeignKey('marriage.id'), nullable=False)
    date_of_divorce = db.Column(db.DateTime, nullable=False)


class Death(db.Model):
    __tablename__ = "death"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_death = db.Column(db.DateTime, nullable=False)


class SexChange(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_change = db.Column(db.DateTime, nullable=False)
    new_sex = db.Column(db.VARCHAR(30), nullable=False)


class Birth(db.Model):
    __tablename__ = "birth"

    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    mother_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)

    father = db.relationship('Person', foreign_keys="Birth.father_id")
    mother = db.relationship('Person', foreign_keys="Birth.mother_id")
    child = db.relationship('Person', foreign_keys="Birth.child_id")


class Adoption(db.Model):
    __tablename__ = "adoption"

    id = db.Column(db.Integer, primary_key=True)
    adoptive_father_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    adoptive_mother_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    adopted_child_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date_of_adopt = db.Column(db.DateTime, nullable=False)

    adoptive_father = db.relationship('Person', foreign_keys="Adoption.adoptive_father_id")
    adoptive_mother = db.relationship('Person', foreign_keys="Adoption.adoptive_mother_id")
    adopted_child = db.relationship('Person', foreign_keys="Adoption.adopted_child_id")


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_change = db.Column(db.DateTime, nullable=False)
    changed_parameter = db.Column(db.String(100), nullable=False)
    changed_value = db.Column(db.String(100), nullable=False)


class Genealogy(db.Model):
    __tablename__ = "genealogy"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    generation = db.Column(db.Integer, nullable=False)

    person = db.relationship('Person', foreign_keys="Genealogy.person_id")
    parent = db.relationship('Person', foreign_keys="Genealogy.parent_id")
