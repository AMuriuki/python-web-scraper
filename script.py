import sys
import requests
import time
from app import app, db
from flask_script import Manager
from bs4 import BeautifulSoup
from app.models import Vehiclemodel, Vehiclemake, Vehiclespecification, Vehiclesystem, Vehiclesubsystem, Vehiclesecondlevelsubsystem, Vehicle3rdlevelsubsystem, Vehiclepart

manager = Manager(app)

@manager.command
def vehicle_make():
    url = "https://partsouq.com/"
    
    while True:
        try:
            print("Connecting to " + url)
            page = requests.get(url)
        except requests.exceptions.ConnectionError:           
            continue
        except requests.exceptions.ChunkedEncodingError:
            continue
        break
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='shop-title')
    print("Fetching records for vehicle makes on partsouq.com")
    for result in results:
        name = result.text.strip()
        make = Vehiclemake(name=name)
        db.session.add(make)
    db.session.commit()
    makes = db.session.query(Vehiclemake).all()
    print(str(len(makes)) +" vehicle makes posted to DB")
    vehicle_model()


@manager.command
def vehicle_model():
    makes = db.session.query(Vehiclemake).all()
    for make in makes:
        print ("Fetching models for " + make.name)
        url = "https://partsouq.com/en/catalog/genuine/locate?c="+make.name
        while True:
            try:
                print("Connecting to " + url)
                page = requests.get(url)
            except requests.exceptions.ConnectionError:           
                continue
            except requests.exceptions.ChunkedEncodingError:
                continue
            break
        soup = BeautifulSoup(page.content, 'html.parser')
        panels = soup.find_all('div', class_='panel panel-default')
        for panel in panels:
            title = panel.find('h4', class_='panel-title')
            panel_body = panel.find('div', class_='panel-body')
            if panel_body:
                sub_titles = panel_body.findChildren("a")
                for sub_title in sub_titles:
                    path = (sub_title['href'])
                    model = Vehiclemodel(name=title.text.strip(), make_id=make.id, series_code=sub_title.text.strip(), path_to_specifications=path)
                    db.session.add(model)
                    db.session.commit()
                    print(make.name + " " + model.name + " posted to DB")
                    # vehicle_specification(path, make.id, model.id)
            else:
                anchor_tag = title.find("a")
                path = anchor_tag['href']
                model = Vehiclemodel(name=title.text.strip(), make_id=make.id, path_to_specifications=path)
                db.session.add(model)
                db.session.commit()
                print(make.name + " " + model.name + " posted to DB")
                # vehicle_specification(path, make.id, model.id)
        print("Waiting for 5 secs before proceeding...")
        time.sleep(3)
    models = db.session.query(Vehiclemodel).all()
    print(str(len(models)) + " vehicle models posted to DB")
    vehicle_specification()


@manager.command
def vehicle_specification():
    models = db.session.query(Vehiclemodel).all()
    for model in models:
        make = db.session.query(Vehiclemake).join(Vehiclemodel).filter(Vehiclemake.id == model.make_id).first()
        print ("Fetching vehicle specification records for " + make.name + " " + model.name + " " + str(model.series_code))
        url = "https://partsouq.com"+model.path_to_specifications
        while True:
            try:
                print("Connecting to " + url)
                page = requests.get(url)
            except requests.exceptions.ConnectionError:           
                continue
            except requests.exceptions.ChunkedEncodingError:
                continue
            break
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
            records.append(cols)

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
                        _model = record[model_index]
                    except:
                        _model = ""

            else:
                _model = ""

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


            vehiclespecification = Vehiclespecification(name=name, year=year, destination_region=destination_region, engine=engine, model=_model, steering=steering, model_id=model.id, make_id=make.id, transmission=transmission, body_style=body_style, series_description=series_description, model_year_from=model_year_from, model_year_to=model_year_to, market=market, grade=grade, path_to_partscatalog=anchor['href'])

            db.session.add(vehiclespecification)
            db.session.commit()
            print("Vehicle specifications for " + make.name + " " + model.name + " posted to DB")
        print("Waiting for 5 secs before proceeding...")
        time.sleep(3)

    specifications = db.session.query(Vehiclespecification).all()
    print(str(len(specifications)) + " records of vehicle specifications posted to DB")


def stringoperation(stringvalue):
    newstring = stringvalue.replace('-', '-parent-')
    return newstring


def get_link_to_systems(path):
    url = "https://partsouq.com"+path
    while True:
        try:
            print("Connecting to " + url)
            page = requests.get(url)
        except requests.exceptions.ConnectionError:           
            continue
        except requests.exceptions.ChunkedEncodingError:
            continue
        break
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
def vehicle_system():
    specifications = db.session.query(Vehiclespecification).filter(id > 16504).all()
    print(len(specifications))
    for specification in specifications:
        make = db.session.query(Vehiclemake).join(Vehiclespecification).filter(Vehiclemake.id == specification.make_id).first()
        model = db.session.query(Vehiclemodel).join(Vehiclespecification).filter(Vehiclemodel.id == specification.model_id).first()
        link = get_link_to_systems(specification.path_to_partscatalog)
        print ("Fetching vehicle part systems for " + make.name + " " + model.name + " " + specification.name + " " + specification.model + " " + specification.series_description)
        url = "https://partsouq.com"+link
        
        while True:
            try:
                print("Connecting to " + url)
                page = requests.get(url)
            except requests.exceptions.ConnectionError:           
                continue
            except requests.exceptions.ChunkedEncodingError:
                continue
            break
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

            vehiclesystem = Vehiclesystem(system=table_col.text.strip(), class_element=_parent_class, make_id=make.id, model_id=model.id, url=url, specification_id = specification.id)

            db.session.add(vehiclesystem)
            
            print("System - "+ table_col.text.strip() +" added")
        db.session.commit()


    systems = db.session.query(Vehiclesystem).all()
    print(str(len(systems)) + " systems posted to DB" )
    vehicle_subsystem()


@manager.command
def vehicle_subsystem():
    vehiclepart_systems = db.session.query(Vehiclesystem).all()
    for vehiclepart_system in vehiclepart_systems:
        make = db.session.query(Vehiclemake).join(Vehiclesystem).filter(Vehiclemake.id == vehiclepart_system.make_id).first()
        model = db.session.query(Vehiclemodel).join(Vehiclesystem).filter(Vehiclemodel.id == vehiclepart_system.model_id).first()
        specification = db.session.query(Vehiclespecification).join(Vehiclesystem).filter(Vehiclespecification.id == vehiclepart_system.specification_id).first()
        
        while True:
            try:
                print("Connecting to " + vehiclepart_system.url)
                page = requests.get(vehiclepart_system.url)
            except requests.exceptions.ConnectionError:           
                continue
            except requests.exceptions.ChunkedEncodingError:
                continue
            break
        soup = BeautifulSoup(page.content, 'html.parser')
        parent_class = stringoperation(vehiclepart_system.class_element)
        for table_row in soup.select('tr[class*="'+parent_class+'"]'):
            table_col = table_row.find('td')

            try:
                #1st level subsystem
                subsystem = table_col.text.strip()
                path_to_parts = table_col.find("a")['href']
                system_id = vehiclepart_system.id
            except:
                #if 2nd level sub-system exists
                vehiclesubsystem = Vehiclesubsystem(subsystem=table_col.text.strip(), path_to_parts=None, system_id=vehiclepart_system.id, class_element=stringoperation(table_row['class'][0]), make_id=make.id, model_id=model.id, specification_id=specification.id)

                db.session.add(vehiclesubsystem)
                db.session.commit()

                # vehicle_2ndlevel_subsystem(vehiclesystem_id, vehiclesubsystem.id, stringoperation(table_row['class'][0]), make_id, model_id, soup)
                
            else:
                vehiclesubsystem = Vehiclesubsystem(subsystem=subsystem, path_to_parts=path_to_parts, system_id=system_id, make_id=make.id, model_id=model.id, specification_id=specification.id)

                db.session.add(vehiclesubsystem)
                db.session.commit()

                print("Subsytem - " + subsystem + " posted to DB")
                vehicle_part(make.id, model.id, path_to_parts, vehiclepart_system.id, vehiclesubsystem.id, None, None, specification.id)
        time.sleep(3)
    subsystems = db.session.query(Vehiclesubsystem).all()
    print(str(len(subsystems)) + " sub systems posted to DB")
    vehicle_2ndlevel_subsystem()



@manager.command
def vehicle_2ndlevel_subsystem():
    vehiclepart_subsystems = db.session.query(Vehiclesubsystem).all()
    for vehiclepart_subsystem in vehiclepart_subsystems:
        make = db.session.query(Vehiclemake).join(Vehiclesubsystem).filter(Vehiclemake.id == vehiclepart_subsystem.make_id).first()
        model = db.session.query(Vehiclemodel).join(Vehiclesubsystem).filter(Vehiclemodel.id == vehiclepart_subsystem.model_id).first()
        vehiclesystem = db.session.query(Vehiclesystem).join(Vehiclesubsystem).filter(Vehiclesystem.id == vehiclepart_subsystem.system_id).first()
        specification = db.session.query(Vehiclespecification).join(Vehiclesubsystem).filter(Vehiclespecification.id == vehiclepart_subsystem.specification_id).first()
        
        if vehiclepart_subsystem.class_element:
            
            while True:
                try:
                    print("Connecting to " + url)
                    page = requests.get(vehiclepart_subsystem.url)
                except requests.exceptions.ConnectionError:           
                    continue
                except requests.exceptions.ChunkedEncodingError:
                    continue
                break
            soup = BeautifulSoup(page.content, 'html.parser')
            parent_class = vehiclepart_subsystem.class_element
            for table_row in soup.select('tr[class*="'+parent_class+'"]'):
                table_col = table_row.find('td')

                try:
                    #2nd level subsystem
                    secondlevel_subsystem = table_col.text.strip()
                    path_to_parts = table_col.find("a")['href']
                    subsystem_id = vehiclepart_subsystem.id
                    system_id = vehiclesystem.id
                except:
                    #if 3rd level sub-system exists
                    vehiclesecondlevelsubsystem = Vehiclesecondlevelsubsystem(secondlevel_subsystem=table_col.text.strip(), subsystem_id=vehiclepart_subsystem.id, system_id=vehiclesystem.id, make_id=make.id, model_id=model.id, class_element=stringoperation(table_row['class'][0]), url=vehiclepart_subsystem.url, specification_id=specification.id)

                    db.session.add(vehiclesecondlevelsubsystem)
                    db.session.commit()
                    
                    # print("3rd level subsystem exists")
                else:
                    vehiclesecondlevelsubsystem = Vehiclesecondlevelsubsystem(secondlevel_subsystem=secondlevel_subsystem, path_to_parts=path_to_parts, subsystem_id=subsystem_id, system_id=system_id, make_id=make.id, model_id=model.id, url=vehiclepart_subsystem.url, specification_id=specification.id)

                    db.session.add(vehiclesecondlevelsubsystem)
                    db.session.commit()

                    print("2nd level sub system - " + secondlevel_subsystem + " added")

                    vehicle_part(make.id, model.id, path_to_parts, vehiclesystem.id, vehiclepart_subsystem.id, vehiclesecondlevelsubsystem.id, None, specification.id)
        time.sleep(3)
    secondlevel_subsystems = db.session.query(Vehiclesecondlevelsubsystem).all()
    print(str(len(secondlevel_subsystems)) + " 2nd level sub systems posted in DB")
    vehicle_3rdlevel_subsystem()            


@manager.command
def vehicle_3rdlevel_subsystem():
    secondlevel_subsystems = db.session.query(Vehiclesecondlevelsubsystem).all()

    for secondlevel_subsystem in secondlevel_subsystems:
        make = db.session.query(Vehiclemake).join(Vehiclesecondlevelsubsystem).filter(Vehiclemake.id == secondlevel_subsystem.make_id).first()
        model = db.session.query(Vehiclemodel).join(Vehiclesecondlevelsubsystem).filter(Vehiclemodel.id == secondlevel_subsystem.model_id).first()
        vehiclesystem = db.session.query(Vehiclesystem).join(Vehiclesecondlevelsubsystem).filter(Vehiclesystem.id == secondlevel_subsystem.system_id).first()
        vehicle_subsystem = db.session.query(Vehiclesubsystem).join(Vehiclesecondlevelsubsystem).filter(Vehiclesubsystem.id == secondlevel_subsystem.subsystem_id).first()
        specification = db.session.query(Vehiclespecification).join(Vehiclesecondlevelsubsystem).filter(Vehiclespecification.id == secondlevel_subsystem.specification_id).first()
        
        if secondlevel_subsystem.class_element:
            
            while True:
                try:
                    print("Connecting to " + secondlevel_subsystem.url)
                    page = requests.get(secondlevel_subsystem.url)
                except requests.exceptions.ConnectionError:           
                    continue
                except requests.exceptions.ChunkedEncodingError:
                    continue
                break
            soup = BeautifulSoup(page.content, 'html.parser')
            for table_row in soup.select('tr[class*="'+secondlevel_subsystem.class_element+'"]'):

                table_col = table_row.find('td')
                try:
                    #3rd level subsystem
                    thirdlevel_subsystem = table_col.text.strip()
                    path_to_parts = table_col.find("a")['href']
                    subsystem_id = vehicle_subsystem.id
                    system_id = vehiclesystem.id
                    secondlevel_subsystem_id = secondlevel_subsystem.id
                except:
                    #if 4th lvel subsystem exists
                    print("4th level subsystem exists")
                else:
                    # print(thirdlevel_subsystem, path_to_parts, subsystem_id, system_id, secondlevel_subsystem_id)

                    vehicle3rdlevelsubsystem = Vehicle3rdlevelsubsystem(thirdlevel_subsystem=thirdlevel_subsystem, path_to_parts=path_to_parts, subsystem_id=subsystem_id, system_id=system_id, secondlevel_subsystem_id=secondlevel_subsystem_id, specification_id=specification.id)

                    db.session.add(vehicle3rdlevelsubsystem)
                    db.session.commit()

                    print("3rd level " +thirdlevel_subsystem +" added")

                    vehicle_part(make.id, model.id, path_to_parts, vehiclesystem.id, vehicle_subsystem.id, secondlevel_subsystem.id, vehicle3rdlevelsubsystem.id, specification.id)


@manager.command
def vehicle_part(make_id, model_id, path_to_parts, vehiclesystem_id, vehiclesubsystem_id, vehiclesecondlevelsubsystem_id, vehicle3rdlevelsubsystem_id, specification_id):
    url = "https://partsouq.com"+path_to_parts
    
    while True:
        try:
            print("Connecting to " + url)
            page = requests.get(url)
        except requests.exceptions.ConnectionError:           
            continue
        except requests.exceptions.ChunkedEncodingError:
            continue
        break
    soup = BeautifulSoup(page.content, 'html.parser')
    part_category = soup.find_all("div", class_='col-lg-12')[1]
    part_subcategory = soup.find("div", class_='col-xs-8 unit-header')
    table = soup.find('table', class_='glow pop-vin table table-bordered-1 table-hover table-condensed')
    rows = table.findAll('tr')
    headers = []
    records = []
    links = []
    for row in rows:
        ths = row.find_all('th')
        for th in ths:
            if th:
                headers.append(th.text.strip())
        cols = row.find_all('td')
        anchor = row.find("a")
        if anchor:
            links.append(anchor['href'])
        _rows = [ele.text.strip() for ele in cols]
        records.append(_rows)

    links = list(filter(None, links)) #Get rid of empty lists
    headers = list(filter(None, headers)) #Get rid of empty lists
    records = list(filter(None, records)) #Get rid of empty lists


    for record, link in zip(records, links):
        number_index = [idx for idx, element in enumerate(headers) if element == "Number"]

        name_index = [idx for idx, element in enumerate(headers) if element == "Name"]

        code_index = [idx for idx, element in enumerate(headers) if element ==
        "Code"]

        qty_required_index = [idx for idx, element in enumerate(headers) if element ==
        "Qty Required"]

        note_index = [idx for idx, element in enumerate(headers) if element ==
        "Note"]

        manufacturer_note_index = [idx for idx, element in enumerate(headers) if element ==
        "Manufacturer_note"]

        end_of_production_index = [idx for idx, element in enumerate(headers) if element ==
        "End_of_production"]

        comment1_index = [idx for idx, element in enumerate(headers) if element ==
        "Comment1"]

        associated_parts_index = [idx for idx, element in enumerate(headers) if element ==
        "Associated_parts"]

        if number_index:
            for _number_index in number_index:
                number_index = int(_number_index)
                try:
                    number = record[number_index]
                except:
                    number = ""
        else:
            number = ""

        if name_index:
            for _name_index in name_index:
                name_index = int(_name_index)
                try:
                    name = record[name_index]
                except:
                    name_index = ""

        else:
            name_index = ""

        if code_index:
            for _code_index in code_index:
                code_index = int(_code_index)
                try:
                    code = record[code_index]
                except:
                    code = ""

        else:
            code = ""

        if qty_required_index:
            for _qty_required_index in qty_required_index:
                qty_required_index = int(_qty_required_index)
                try:
                    qty_required = record[qty_required_index]
                except:
                    qty_required = ""

        else:
            qty_required = ""

        if note_index:
            for _note_index in note_index:
                note_index = int(_note_index)
                try:
                    note = record[note_index]
                except:
                    note = ""

        else:
            note = ""

        if manufacturer_note_index:
            for _manufacturer_note_index in manufacturer_note_index:
                manufacturer_note_index = int(_manufacturer_note_index)
                try:
                    manufacturer_note = record[manufacturer_note_index]
                except:
                    manufacturer_note = ""

        else:
            manufacturer_note = ""

        if end_of_production_index:
            for _end_of_production_index in end_of_production_index:
                end_of_production_index = int(_end_of_production_index)
                try:
                    end_of_production = record[end_of_production_index]
                except:
                    end_of_production = ""

        else:
            end_of_production = ""

        if comment1_index:
            for _comment1_index in comment1_index:
                comment1_index = int(_comment1_index)
                try:
                    comment1 = record[comment1_index]
                except:
                    comment1 = ""

        else:
            comment1 = ""

        if associated_parts_index:
            for _associated_parts_index in associated_parts_index:
                associated_parts_index = int(_associated_parts_index)
                try:
                    associated_parts = record[associated_parts_index]
                except:
                    associated_parts = ""

        else:
            associated_parts = ""

        vehiclepart = Vehiclepart(part_category=part_category.text.strip(), part_subcategory=part_subcategory.text.strip(), part_number=number, part_name=name, part_code=code, qty_required=qty_required, note=note, manufacturer_note=manufacturer_note, end_of_production=end_of_production, comment=comment1, associated_parts=associated_parts, path_to_cost=link, system_id=vehiclesystem_id, subsystem_id=vehiclesubsystem_id, secondlevel_subsystem_id=vehiclesecondlevelsubsystem_id, thirdlevel_subsystem_id=vehicle3rdlevelsubsystem_id, model_id=model_id, make_id=make_id, specification_id=specification_id)

        db.session.add(vehiclepart)
        db.session.commit()

if __name__ == "__main__":
    manager.run()
