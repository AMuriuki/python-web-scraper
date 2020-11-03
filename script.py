import sys
import requests
from app import app, db
from flask_script import Manager
from bs4 import BeautifulSoup


manager = Manager(app)


class Vehiclemake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    models = db.relationship('Vehiclemodel', backref='make', lazy='dynamic')

    def __repr__(self):
        return '<Make {}>'.format(self.name)


class Vehiclemodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    make_id = db.Column(db.Integer, db.ForeignKey('vehiclemake.id'))
    series = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Model {}>'.format(self.name)


@manager.command
def vehicle_make():
    url = "https://partsouq.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='shop-title')
    for result in results:
        name = result.text.strip()
        make = Vehiclemake(name=name)
        db.session.add(make)
        print ("Adding "+ name)
        vehicle_model(name)
    db.session.commit()
    print("success")


@manager.command
def vehicle_model(name):
    make = db.session.query(Vehiclemake).filter_by(name=name).first()
    url = "https://partsouq.com/en/catalog/genuine/locate?c="+name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    panels = soup.find_all('div', class_='panel panel-default')
    for panel in panels:
        title = panel.find('h4', class_='panel-title')
        panel_body = panel.find('div', class_='panel-body')
        if panel_body:
            sub_titles = panel_body.findChildren("a")
            for sub_title in sub_titles:
                # print (title.text.strip(), sub_title.text.strip())
                print ("Adding " + name + " " + title.text.strip() + " " + sub_title.text.strip())
                model = Vehiclemodel(name=title.text.strip(), make_id=make.id, series=sub_title.text.strip())
                db.session.add(model)                
        else:
            print (title.text.strip())
            print ("Adding " + name + " " + title.text.strip())
            model = Vehiclemodel(name=title.text.strip(), make_id=make.id)
            db.session.add(model)                
    db.session.commit()   
        

if __name__ == "__main__":
    manager.run()
