import sys
import requests
from app import app, db
from flask_script import Manager
from bs4 import BeautifulSoup
from app.models import Vehiclemodel, Vehiclemake, Vehiclespecification, Vehiclesystem, Vehiclesubsystem, Vehiclesecondlevelsubsystem, Vehicle3rdlevelsubsystem

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
                model = Vehiclemodel(name=title.text.strip(), make_id=make.id, series_code=sub_title.text.strip(), path_to_specifications=path)
                db.session.add(model)  
                db.session.commit()       
                vehicle_specification(path, make.id, model.id)        
        else:
            anchor_tag = title.find("a") 
            path = anchor_tag['href']
            print ("Adding " + name + " " + title.text.strip())
            model = Vehiclemodel(name=title.text.strip(), make_id=make.id, path_to_specifications=path)
            db.session.add(model) 
            db.session.commit() 
            vehicle_specification(path, make.id, model.id)
    


@manager.command
def vehicle_specification(path, make_id, model_id):
    url = "https://partsouq.com"+path
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
        anchor = row.find("a")
        cols = [ele.text.strip() for ele in cols]
        records.append(cols) # Get rid of empty values
    
    headers = list(filter(None, headers)) #Get rid of empty lists
    records = list(filter(None, records)) #Get rid of empty lists

    
    for record in records:
        name_index = [idx for idx, element in enumerate(headers) if element == "Name"]

        model_index = [idx for idx, element in enumerate(headers) if element == "Model"]

        destination_region_index = [idx for idx, element in enumerate(headers) if element == 
        "Destination Region"]

        model_year_from_index = [idx for idx, element in enumerate(headers) if element == 
        "Model Year From"]

        model_year_to_index = [idx for idx, element in enumerate(headers) if element == 
        "Model Year To"]

        market_index = [idx for idx, element in enumerate(headers) if element == 
        "Market"]

        grade_index = [idx for idx, element in enumerate(headers) if element == 
        "Grade"]

        series_description_index = [idx for idx, element in enumerate(headers) if element == 
        "Series Description"]

        body_style_index = [idx for idx, element in enumerate(headers) if element == 
        "Body Style"]

        steering_index = [idx for idx, element in enumerate(headers) if element == 
        "Steering"]

        year_index = [idx for idx, element in enumerate(headers) if element == 
        "Model Year"]

        engine_index = [idx for idx, element in enumerate(headers) if element == 
        "Engine"]

        transmission_index = [idx for idx, element in enumerate(headers) if element == 
        "Transmission"]

        if name_index:
            for _name_index in name_index:
                name_index = int(_name_index)
                try:
                    name = record[name_index]
                except:
                    name = ""                
        else:
            name = ""

        if model_year_from_index:
            for _model_year_from_index in model_year_from_index:
                model_year_from_index = int(_model_year_from_index)
                try:
                    model_year_from = record[model_year_from_index]
                except:
                    model_year_from = ""
                
        else:
            model_year_from = ""

        if model_year_to_index:
            for _model_year_to_index in model_year_to_index:
                model_year_to_index = int(_model_year_to_index)
                try:
                    model_year_to = record[model_year_to_index]
                except:
                    model_year_to = ""
                
        else:
            model_year_to = ""

        if market_index:
            for _market_index in market_index:
                market_index = int(_market_index)
                try:
                    market = record[market_index]
                except:
                    market = ""
                
        else:
            market = ""

        if grade_index:
            for _grade_index in grade_index:
                grade_index = int(_grade_index)
                try:
                    grade = record[grade_index]
                except:
                    grade = ""
                
        else:
            grade = ""

        if model_index:
            for _model_index in model_index:
                model_index = int(_model_index)
                try:
                    model = record[model_index]
                except:
                    model = ""
                
        else:
            model = ""

        if series_description_index:
            for _series_description_index in series_description_index:
                series_description_index = int(_series_description_index)
                try:
                    series_description = record[series_description_index]
                except:
                    series_description = ""
                
        else:
            series_description = ""
            
        if destination_region_index:
            for _destination_region_index in destination_region_index:
                destination_region_index = int(_destination_region_index)
                try:
                    destination_region = record[destination_region_index] 
                except:
                    destination_region = ""
                
        else:
            destination_region = ""

        if engine_index:
            for _engine_index in engine_index:
                engine_index = int(_engine_index)
                try:
                    engine = record[engine_index] 
                except:
                    engine = ""
                
        else:
            engine = ""  

        if transmission_index:
            for _transmission_index in transmission_index:
                transmission_index = int(_transmission_index)
                try:
                    transmission = record[transmission_index] 
                except:
                    transmission = ""
                
        else:
            transmission = ""  

        if body_style_index:
            for _body_style_index in body_style_index:
                body_style_index = int(_body_style_index)
                
                try:
                    body_style = record[body_style_index] 
                except:
                    body_style = ""
                
        else:
            body_style = ""

        if steering_index:
            for _steering_index in steering_index:
                steering_index = int(_steering_index)
                steering = record[steering_index] 
                
        else:
            steering = ""
    
        if year_index:
            for _year_index in year_index:
                year_index = int(_year_index)
                try:
                    year = record[year_index] 
                except:
                    year = ""
                
        else:
            year = ""       
                  

        vehiclespecification = Vehiclespecification(name=name, year=year, destination_region=destination_region, engine=engine, model=model, steering=steering, model_id=model_id, make_id=make_id, transmission=transmission, body_style=body_style, series_description=series_description, model_year_from=model_year_from, model_year_to=model_year_to, market=market, grade=grade, path_to_partscatalog=anchor['href'])

        db.session.add(vehiclespecification)

        vehicle_system(path, make_id, model_id)
    db.session.commit()
    


def stringoperation(stringvalue):
    newstring = stringvalue.replace('-', '-parent-')
    return newstring


def get_link_to_systems(path):
    url = "https://partsouq.com"+path
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    catalog_groups = soup.find('div', class_='catalog-groups')
    nav_tags = catalog_groups.findChildren("ul")
    for nav_tag in nav_tags:
        link_tags = nav_tag.find_all("li")
        for link_tag in link_tags:
            anchor_tag = link_tag.find("a")
            if anchor_tag.text.strip() == "Groups":
                link = anchor_tag['href']
                break
    return link


@manager.command
def vehicle_system(path, make_id, model_id):
    link = get_link_to_systems(path)    
    url = "https://partsouq.com"+link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='table-mage group-main1 table table-bordered-1 table-stripped tree')
    rows = table.findAll('tr', class_=True)
    parent_classes = []
    child_classes = []
    for row in rows:
        if len(row.attrs['class']) == 1:
            parent_classes.append(row.attrs['class'])
        
    _parent_classes = []
    for parent_class in parent_classes:
        for _parent_class in parent_class:
            _parent_classes.append(_parent_class)

    # print(_parent_classes)
    for _parent_class in _parent_classes:
        table_row = table.find('tr', class_=_parent_class)
        table_col = table_row.find('td')
        
        vehiclesystem = Vehiclesystem(system=table_col.text.strip(), class_element=_parent_class)

        db.session.add(vehiclesystem)
        db.session.commit()

        print("System "+ table_col.text.strip() +" added")

        vehicle_subsystem(vehiclesystem.id, _parent_class, make_id, model_id, soup)    


@manager.command
def vehicle_subsystem(vehiclesystem_id, parentclass, make_id, model_id, soup):
    parent_class = stringoperation(parentclass)
    for table_row in soup.select('tr[class*="'+parent_class+'"]'):
        table_col = table_row.find('td')

        try:
            #1st level subsystem
            subsystem = table_col.text.strip()
            path_to_parts = table_col.find("a")['href']
            system_id = vehiclesystem_id
        except:
            #if 2nd level sub-system exists
            vehiclesubsystem = Vehiclesubsystem(subsystem=table_col.text.strip(), path_to_parts=None, system_id=vehiclesystem_id)

            db.session.add(vehiclesubsystem)
            db.session.commit()

            vehicle_2ndlevel_subsystem(vehiclesystem_id, vehiclesubsystem.id, stringoperation(table_row['class'][0]), make_id, model_id, soup)
            print("2nd level subsystem exists")
        else:
            vehiclesubsystem = Vehiclesubsystem(subsystem=subsystem, path_to_parts=path_to_parts, system_id=system_id)

            db.session.add(vehiclesubsystem)
            db.session.commit()

            print("Subsytem " + subsystem + " added")    
            vehicle_part(make_id, model_id, path_to_parts, vehiclesystem_id, vehiclesubsystem.id, None, None)
            

@manager.command
def vehicle_part(make_id, model_id, path_to_parts, vehiclesystem_id, vehiclesubsystem_id, vehiclesecondlevelsubsystem_id, vehicle3rdlevelsubsystem_id):
    url = "https://partsouq.com"+path_to_parts
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    part_title = soup.find_all("div", class_='col-lg-12')[1]
    print(part_title.text.strip())



@manager.command
def vehicle_2ndlevel_subsystem(vehiclesystem_id ,vehiclesubsystem_id, parentclass, make_id, model_id, soup):
    parent_class = parentclass
    for table_row in soup.select('tr[class*="'+parent_class+'"]'):
        table_col = table_row.find('td')

        try:
            #2nd level subsystem
            secondlevel_subsystem = table_col.text.strip()
            path_to_parts = table_col.find("a")['href']
            subsystem_id = vehiclesubsystem_id
            system_id = vehiclesystem_id            
        except:
            #if 3rd level sub-system exists
            vehiclesecondlevelsubsystem = Vehiclesecondlevelsubsystem(secondlevel_subsystem=table_col.text.strip(), subsystem_id=vehiclesubsystem_id, system_id=vehiclesystem_id)

            db.session.add(vehiclesecondlevelsubsystem)
            db.session.commit()

            vehicle_3rdlevel_subsystem(vehiclesystem_id, vehiclesubsystem_id, vehiclesecondlevelsubsystem.id, stringoperation(table_row['class'][0]), make_id, model_id, soup)
            print("3rd level subsystem exists")
        else:
            vehiclesecondlevelsubsystem = Vehiclesecondlevelsubsystem(secondlevel_subsystem=secondlevel_subsystem, path_to_parts=path_to_parts, subsystem_id=subsystem_id, system_id=system_id)

            db.session.add(vehiclesecondlevelsubsystem)
            db.session.commit()

            print("2nd level sub system " + secondlevel_subsystem + " added")    

            vehicle_part(make_id, model_id, path_to_parts, vehiclesystem_id, vehiclesubsystem_id, vehiclesecondlevelsubsystem.id, None)


@manager.command
def vehicle_3rdlevel_subsystem(vehiclesystem_id, vehiclesubsystem_id, vehiclesecondlevelsubsystem_id, parentclass, make_id, model_id, soup):
    for table_row in soup.select('tr[class*="'+parentclass+'"]'):
        table_col = table_row.find('td')
        try:
            #3rd level subsystem
            thirdlevel_subsystem = table_col.text.strip() 
            path_to_parts = table_col.find("a")['href']
            subsystem_id = vehiclesubsystem_id
            system_id = vehiclesystem_id 
            secondlevel_subsystem_id = vehiclesecondlevelsubsystem_id
        except:        
            #if 4th lvel subsystem exists
            print("4th level subsystem exists")
        else:
            # print(thirdlevel_subsystem, path_to_parts, subsystem_id, system_id, secondlevel_subsystem_id)

            vehicle3rdlevelsubsystem = Vehicle3rdlevelsubsystem(thirdlevel_subsystem=thirdlevel_subsystem, path_to_parts=path_to_parts, subsystem_id=subsystem_id, system_id=system_id, secondlevel_subsystem_id=secondlevel_subsystem_id)

            db.session.add(vehicle3rdlevelsubsystem)
            db.session.commit()

            print("3rd level " +thirdlevel_subsystem +" added")
            
            vehicle_part(make_id, model_id, path_to_parts, vehiclesystem_id, vehiclesubsystem_id, vehiclesecondlevelsubsystem_id, vehicle3rdlevelsubsystem.id)


if __name__ == "__main__":
    manager.run()
