import sys
import requests
from app import app, db
from flask_script import Manager
from bs4 import BeautifulSoup
from app.models import Vehiclemodel, Vehiclemake, Vehiclespecification

manager = Manager(app)

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
        # if name:
        #     break
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
                print ("Adding " + name + " " + title.text.strip() + " " + sub_title.text.strip())
                path = (sub_title['href'])
                vehicle_details(path)
                model = Vehiclemodel(name=title.text.strip(), make_id=make.id, series_code=sub_title.text.strip(), path_to_details=path)
                db.session.add(model)                
        else:
            anchor_tag = title.find("a") 
            path = anchor_tag['href']
            print ("Adding " + name + " " + title.text.strip())
            vehicle_details(path)
            model = Vehiclemodel(name=title.text.strip(), make_id=make.id, path_to_details=path)
            db.session.add(model)        
    db.session.commit()
    print("success")


@manager.command
def vehicle_details(path):
    url = "https://partsouq.com/"+path
    print ("Vehicle details on "+url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='table table-hover mb-0px')
    rows = table.findAll('tr')
    headers = []
    records = []
    for row in rows:
        ths = row.find_all('th')
        for th in ths:
            if th:
                headers.append(th.text.strip())                
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        records.append([ele for ele in cols if ele]) # Get rid of empty values
    
    headers = list(filter(None, headers)) #Get rid of empty lists
    records = list(filter(None, records)) #Get rid of empty lists

    for record in records:
        name_index = [idx for idx, element in enumerate(headers) if element == "Name"]

        model_index = [idx for idx, element in enumerate(headers) if element == "Model"]

        region_index = [idx for idx, element in enumerate(headers) if element == 
        "Destination Region"]

        body_style_index = [idx for idx, element in enumerate(headers) if element == 
        "Body Style"]

        steering_index = [idx for idx, element in enumerate(headers) if element == 
        "Steering"]

        year_index = [idx for idx, element in enumerate(headers) if element == 
        "Model Year"]

        engine_index = [idx for idx, element in enumerate(headers) if element == 
        "Engine"]

        if name_index:
            for _name_index in name_index:
                name_index = int(_name_index)
                name = record[name_index]
                print(name)
        else:
            name = ""

        if model_index:
            for _model_index in model_index:
                model_index = int(_model_index)
                model = record[model_index]
                print(model)
        else:
            model = ""
            
        if region_index:
            for _region_index in region_index:
                region_index = int(_region_index)
                region = record[region_index] 
                print(region)
        else:
            region = ""

        if body_style_index:
            for _body_style_index in body_style_index:
                body_style_index = int(_body_style_index)
                body_style = record[body_style_index] 
                print(body_style)
        else:
            body_style = ""

        if steering_index:
            for _steering_index in steering_index:
                steering_index = int(_steering_index)
                steering = record[steering_index] 
                print(steering)
        else:
            steering = ""
    
        if year_index:
            for _year_index in year_index:
                year_index = int(_year_index)
                year = record[year_index] 
                print(year)
        else:
            year = ""
        
        if engine_index:
            for _engine_index in engine_index:
                engine_index = int(_engine_index)
                engine = record[engine_index] 
                print(engine)
        else:
            engine = ""            

        vehiclespecification = Vehiclespecification(name=name, year=year, region=region, engine=engine, model=model, steering=steering, model_id=1, make_id=1)

        db.session.add(vehiclespecification)
    db.session.commit()
    print("success")


if __name__ == "__main__":
    manager.run()
