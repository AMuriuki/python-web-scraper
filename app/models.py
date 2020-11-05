from app import db

class Vehiclemake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    models = db.relationship('Vehiclemodel', backref='vehiclemake.id', lazy='dynamic')
    specifications = db.relationship('Vehiclespecification', backref='vehiclemake.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclemake.id', lazy='dynamic')

    def __repr__(self):
        return '<Make {}>'.format(self.name)


class Vehiclemodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    series_code = db.Column(db.String(64), index=True) 
    specifications = db.relationship('Vehiclespecification', backref='vehiclemodel.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclemodel.id', lazy='dynamic')
    path_to_specifications = db.Column(db.Text(), index=True)

    def __repr__(self):
        return '<Model {}>'.format(self.name)


class Vehiclespecification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    region = db.Column(db.String(64), index=True)
    engine = db.Column(db.String(64), index=True)
    model = db.Column(db.String(64), index=True)
    body_style = db.Column(db.String(64), index=True)
    steering = db.Column(db.String(64), index=True)
    year = db.Column(db.String(64), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))


class Vehiclepart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(64), index=True)
    part_name = db.Column(db.String(64), index=True)
    cost = db.Column(db.String(64), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id')) 


    