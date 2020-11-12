from app import db

class Vehiclemake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    models = db.relationship('Vehiclemodel', backref='vehiclemake.id', lazy='dynamic')
    specifications = db.relationship('Vehiclespecification', backref='vehiclemake.id', lazy='dynamic')
    
    def __repr__(self):
        return '<Make {}>'.format(self.name)


class Vehiclemodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    series_code = db.Column(db.String(64), index=True) 
    specifications = db.relationship('Vehiclespecification', backref='vehiclemodel.id', lazy='dynamic')
    path_to_specifications = db.Column(db.Text(), index=True)
    
    def __repr__(self):
        return '<Model {}>'.format(self.name)


class Vehiclespecification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    destination_region = db.Column(db.String(64), index=True)
    engine = db.Column(db.String(64), index=True)
    model = db.Column(db.String(64), index=True)
    body_style = db.Column(db.String(64), index=True)
    steering = db.Column(db.String(64), index=True)
    year = db.Column(db.String(64), index=True)
    model_year_from = db.Column(db.String(64), index=True)
    model_year_to = db.Column(db.String(64), index=True)
    market = db.Column(db.String(64), index=True)
    grade = db.Column(db.String(64), index=True)
    transmission = db.Column(db.String(64), index=True)
    series_description = db.Column(db.String(64), index=True)
    path_to_partscatalog = db.Column(db.Text(), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    systemdetails = db.relationship('Vehiclesystemdetails', backref='vehiclespecification.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclespecification.id', lazy='dynamic')


class Vehiclesystemparts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.String(64), index=True)
    systemdetails = db.relationship('Vehiclesystemdetails', backref='vehiclesystemparts.id', lazy='dynamic')
    class_element = db.Column(db.String(64), index=True)    


class Vehiclesystemdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystemparts.id'))
    subsystem = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.Text(), index=True)
    specification_id = db.Column(db.Integer, db.ForeignKey('vehiclespecification.id'))
    

class Vehiclepart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_category = db.Column(db.String(64), index=True)
    part_subcategory = db.Column(db.String(64), index=True)
    part_number = db.Column(db.String(64), index=True)
    part_name = db.Column(db.String(64), index=True)
    part_code = db.Column(db.String(64), index=True)
    qty_required = db.Column(db.String(64), index=True)
    note = db.Column(db.String(64), index=True)
    manufacturer_note = db.Column(db.String(64), index=True)
    end_of_production = db.Column(db.String(64), index=True)
    comment = db.Column(db.String(64), index=True)
    associated_parts = db.Column(db.String(64), index=True)
    path_to_cost = db.Column(db.Text(), index=True)
    cost = db.Column(db.String(64), index=True)
    specification_id = db.Column(db.Integer, db.ForeignKey('vehiclespecification.id'))

    