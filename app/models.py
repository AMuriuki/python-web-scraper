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


class Vehiclesystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.String(64), index=True)
    class_element = db.Column(db.String(64), index=True)
    subsystems = db.relationship('Vehiclesubsystem', backref='vehiclesystem.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclesystem.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclesystem.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclesystem.id', lazy='dynamic')
    

class Vehiclesubsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subsystem = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.String(64), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    parts = db.relationship('Vehiclepart', backref='vehiclesubsystem.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclesubsystem.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclesubsystem.id', lazy='dynamic')


class Vehiclesecondlevelsubsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secondlevel_subsystem = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.String(64), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesubsystem.id'))
    parts = db.relationship('Vehiclepart', backref='vehiclesecondlevelsubsystem.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclesecondlevelsubsystem.id', lazy='dynamic')


class Vehicle3rdlevelsubsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thirdlevel_subsystem = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.String(64), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesubsystem.id'))
    secondlevel_subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesecondlevelsubsystem.id'))
    parts = db.relationship('Vehiclepart', backref='vehicle3rdlevelsubsystem.id', lazy='dynamic')

# class Vehiclepartcategory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     system = db.Column(db.String(64), index=True)
#     category = db.Column(db.String(64), index=True)
#     subcategory = db.Column(db.String(64), index=True)
#     _subcategory = db.Column(db.String(64), index=True)
#     parts = db.relationship('Vehiclepart', backref='vehiclepartcategory.id', lazy='dynamic')
    

class Vehiclepart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(64), index=True)
    part_name = db.Column(db.String(64), index=True)
    cost = db.Column(db.String(64), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesubsystem.id'))
    secondlevel_subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesecondlevelsubsystem.id'))
    thirdlevel_subsystem_id = db.Column(db.Integer, db.ForeignKey('vehicle3rdlevelsubsystem.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id')) 

    