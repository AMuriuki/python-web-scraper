from app import db

class Vehiclemake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    models = db.relationship('Vehiclemodel', backref='vehiclemake.id', lazy='dynamic')
    specifications = db.relationship('Vehiclespecification', backref='vehiclemake.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclemake.id', lazy='dynamic')
    systems = db.relationship('Vehiclesystem', backref='vehiclemake.id', lazy='dynamic')
    subsystems = db.relationship('Vehiclesubsystem', backref='vehiclemake.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclemake.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclemake.id', lazy='dynamic')

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
    systems = db.relationship('Vehiclesystem', backref='vehiclemodel.id', lazy='dynamic')
    subsystems = db.relationship('Vehiclesubsystem', backref='vehiclemodel.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclemodel.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclemodel.id', lazy='dynamic')

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
    systems = db.relationship('Vehiclesystem', backref='vehiclespecification.id', lazy='dynamic')
    subsystems = db.relationship('Vehiclesubsystem', backref='vehiclespecification.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclespecification.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclespecification.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclespecification.id', lazy='dynamic')


class Vehiclesystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.String(64), index=True)
    class_element = db.Column(db.String(64), index=True)
    subsystems = db.relationship('Vehiclesubsystem', backref='vehiclesystem.id', lazy='dynamic')
    parts = db.relationship('Vehiclepart', backref='vehiclesystem.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclesystem.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclesystem.id', lazy='dynamic')
    url = db.Column(db.Text(), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    specification_id = db.Column(db.Integer, db.ForeignKey('vehiclespecification.id'))


class Vehiclesubsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subsystem = db.Column(db.String(64), index=True)
    class_element = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.Text(), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    parts = db.relationship('Vehiclepart', backref='vehiclesubsystem.id', lazy='dynamic')
    secondlevel_subsystems = db.relationship('Vehiclesecondlevelsubsystem', backref='vehiclesubsystem.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclesubsystem.id', lazy='dynamic')
    url = db.Column(db.Text(), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    specification_id = db.Column(db.Integer, db.ForeignKey('vehiclespecification.id'))


class Vehiclesecondlevelsubsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secondlevel_subsystem = db.Column(db.String(64), index=True)
    class_element = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.Text(), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesubsystem.id'))
    parts = db.relationship('Vehiclepart', backref='vehiclesecondlevelsubsystem.id', lazy='dynamic')
    thirdlevel_subsystems = db.relationship('Vehicle3rdlevelsubsystem', backref='vehiclesecondlevelsubsystem.id', lazy='dynamic')
    url = db.Column(db.Text(), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    specification_id = db.Column(db.Integer, db.ForeignKey('vehiclespecification.id'))


class Vehicle3rdlevelsubsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thirdlevel_subsystem = db.Column(db.String(64), index=True)
    path_to_parts = db.Column(db.Text(), index=True)
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesubsystem.id'))
    secondlevel_subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesecondlevelsubsystem.id'))
    parts = db.relationship('Vehiclepart', backref='vehicle3rdlevelsubsystem.id', lazy='dynamic')
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    url = db.Column(db.Text(), index=True)
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
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
    system_id = db.Column(db.Integer, db.ForeignKey('vehiclesystem.id'))
    subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesubsystem.id'))
    secondlevel_subsystem_id = db.Column(db.Integer, db.ForeignKey('vehiclesecondlevelsubsystem.id'))
    thirdlevel_subsystem_id = db.Column(db.Integer, db.ForeignKey('vehicle3rdlevelsubsystem.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('vehiclemodel.id'))
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id')) 
    specification_id = db.Column(db.Integer, db.ForeignKey('vehiclespecification.id'))

    