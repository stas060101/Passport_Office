from passport_office import db


class Person(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(30), nullable=False)

    marriage = db.relationship('Marriage', backref='person')
    death = db.relationship('Death', backref='person')
    sex_change = db.relationship('SexChange', backref='person')
    birth = db.relationship('Birth', backref='person')
    adoption = db.relationship('Adoption', backref='person')
    history = db.relationship('History', backref='person')
    genealogy = db.relationship('Genealogy', backref='person')


class Marriage(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    husband_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    wife_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date_of_marriage = db.Column(db.DateTime, nullable=False)

    divorce = db.relationship('Divorce', backref='marriage')


class Divorce(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    marriage_id = db.Column(db.Integer, db.ForeignKey('marriage.id'), nullable=False)
    date_of_divorce = db.Column(db.DateTime, nullable=False)


class Death(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_death = db.Column(db.DateTime, nullable=False)


class SexChange(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_change = db.Column(db.DateTime, nullable=False)
    new_sex = db.Column(db.VARCHAR(30), nullable=False)


class Birth(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    mother_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)


class Adoption(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    adoptive_father_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    adoptive_mother_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    adopted_child_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    date_of_adopt = db.Column(db.DateTime, nullable=False)


class History(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    date_of_change = db.Column(db.DateTime, nullable=False)
    changed_parameter = db.Column(db.VARCHAR(100), nullable=False)
    changed_value = db.Column(db.VARCHAR(100), nullable=False)


class Genealogy(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    generation = db.Column(db.Integer, nullable=False)
