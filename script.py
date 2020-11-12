import sys
import requests
import time
from app import app, db
from flask_script import Manager
from bs4 import BeautifulSoup
from app.models import Vehiclemodel, Vehiclemake, Vehiclespecification, Vehiclepart, Vehiclesystemparts, Vehiclesystemdetails

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
        links = []
        for row in rows:
            ths = row.find_all('th')
            for th in ths:
                if th:
                    headers.append(th.text.strip())
            cols = row.find_all('td')
            if cols:
                link = cols[1].find("a").get('href')
                links.append(link)            
            cols = [ele.text.strip() for ele in cols]
            records.append(cols)

        headers = list(filter(None, headers)) #Get rid of empty lists
        records = list(filter(None, records)) #Get rid of empty lists
        links = list(filter(None, links)) #Get rid of empty lists
        
        if len(records) == len(links):
            print("Number of links is equal to number of records")
        else:
            raise Exception("Number of links not equal to number of records")

        for record, link in zip(records, links):
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

            print("Getting link to parts catalog for " + make.name + " " + model.name + " " + str(model.series_code))
            link = get_link_to_systems(link)
            
            vehiclespecification = Vehiclespecification(name=name, year=year, destination_region=destination_region, engine=engine, model=_model, steering=steering, model_id=model.id, make_id=make.id, transmission=transmission, body_style=body_style, series_description=series_description, model_year_from=model_year_from, model_year_to=model_year_to, market=market, grade=grade, path_to_partscatalog=link)

            db.session.add(vehiclespecification)
            db.session.commit()
            print("Vehicle specifications for " + make.name + " " + model.name + " posted to DB")
        print("Waiting for 5 secs before proceeding...")
        time.sleep(3)

    specifications = db.session.query(Vehiclespecification).all()
    print(str(len(specifications)) + " vehicle specifications posted to DB")
    vehicle_systems()


def stringoperation(stringvalue):
    newstring = stringvalue.replace('-', '-parent-')
    return newstring


def get_link_to_systems(path):
    url = "https://partsouq.com"+path
    while True:
        try:
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
def vehicle_systems():
    vehiclesystemparts = db.session.query(Vehiclesystemparts).all()
    
    if vehiclesystemparts:
        pass
    else:
        url = "https://partsouq.com/en/catalog/genuine/groups?c=BMW&ssd=%24%2AKwFiVkdEP2MXET5ge2R8UjouDgkXZmlkZXdxfjg4NTs1ES12ZG5_cnFsd3JkZ2U_MTl8cXQjM3N2biklThFgZ3UtAAAAAIq75YA%24&vid=331494080&cid=&q="

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

            vehiclesystemparts = Vehiclesystemparts(system=table_col.text.strip(), class_element=_parent_class)
            db.session.add(vehiclesystemparts)
            
            print("System - "+ table_col.text.strip() +" added")
        db.session.commit()

    systems = db.session.query(Vehiclesystemparts).all()
    print(str(len(systems)) + " systems posted to DB" )
    vehicle_systemdetails()


@manager.command
def vehicle_systemdetails():
    specifications = db.session.query(Vehiclespecification).all()
    systems = db.session.query(Vehiclesystemparts).all()
    for specification in specifications:
        make = db.session.query(Vehiclemake).join(Vehiclespecification).filter(Vehiclemake.id == specification.make_id).first()
        model = db.session.query(Vehiclemodel).join(Vehiclespecification).filter(Vehiclemodel.id == specification.model_id).first()
        print ("Fetching vehicle system details for " + make.name + " " + model.name + " " + specification.name + " " + specification.model + " " + specification.series_description)
        url = "https://partsouq.com"+specification.path_to_partscatalog 
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
        a = 0
        for system in systems:
            if a >= 1: 
                break
            a += 1        
            parent_class = stringoperation(system.class_element)
            for table_row in soup.select('tr[class*="'+parent_class+'"]'):
                table_col = table_row.find('td')

                try:
                    subsystem = table_col.text.strip()
                    path_to_parts = table_col.find("a")['href']
                    system_id = system.id

                    vehiclesystemdetails = Vehiclesystemdetails(system_id=system_id, subsystem=subsystem, path_to_parts=path_to_parts, specification_id=specification.id)
                    db.session.add(vehiclesystemdetails)
                    db.session.commit()

                    print("System details for " + make.name + " " + model.name + " " + specification.name + " " + specification.model + " " + specification.series_description + " added")
                except TypeError:
                    class_element=stringoperation(table_row['class'][0]),
                    
                    for cols in soup.select('tr[class*="'+class_element[0]+'"]'):
                        anchor = cols.find('a')
                        if anchor:
                            subsystem = anchor.text.strip()
                            path_to_parts = anchor['href']
                            vehiclesystemdetails = Vehiclesystemdetails(system_id=system_id, subsystem=subsystem, path_to_parts=path_to_parts, specification_id=specification.id)
                            db.session.add(vehiclesystemdetails)
                            db.session.commit()

                            print("System details for " + make.name + " " + model.name + " " + specification.name + " " + specification.model + " " + specification.series_description + " added")
        time.sleep(3)
        print("Waiting for 5 secs before proceeding...")
    
    systemdetails = db.session.query(Vehiclesystemdetails).all()
    print(str(len(systemdetails)) + " system details posted to DB")
    vehicle_parts()
  

@manager.command
def vehicle_parts():
    systemdetails = db.session.query(Vehiclesystemdetails).all()
    
    for systemdetail in systemdetails:
        specification = db.session.query(Vehiclespecification).join(Vehiclesystemdetails).filter(Vehiclespecification.id == systemdetail.specification_id).first()

        make = db.session.query(Vehiclemake).join(Vehiclespecification).filter(Vehiclemake.id == specification.make_id).first()

        model = db.session.query(Vehiclemodel).join(Vehiclespecification).filter(Vehiclemodel.id == specification.model_id).first()

        system = db.session.query(Vehiclesystemparts).join(Vehiclesystemdetails).filter(Vehiclesystemparts.id == Vehiclesystemdetails.system_id).first()

        print ("Fetching " + system.system + " - " + systemdetail.subsystem  + " for " + make.name + " " + model.name + " " + specification.name + " " + specification.model + " " + specification.series_description + " " + specification.year)
        
        url = "https://partsouq.com"+systemdetail.path_to_parts
    
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

            vehiclepart = Vehiclepart(part_category=part_category.text.strip(), part_subcategory=part_subcategory.text.strip(), part_number=number, part_name=name, part_code=code, qty_required=qty_required, note=note, manufacturer_note=manufacturer_note, end_of_production=end_of_production, comment=comment1, associated_parts=associated_parts, path_to_cost=link, specification_id=specification.id)

            db.session.add(vehiclepart)
            db.session.commit()

            print (system.system + " - " + systemdetail.subsystem  + " for " + make.name + " " + model.name + " " + specification.name + " " + specification.model + " " + specification.series_description + " " + specification.year + " posted to DB")

        print("Waiting for 5 secs before proceeding...")
        time.sleep(3)
    
    systemdetails = db.session.query(Vehiclesystemdetails).all()
    print(str(len(systemdetails)) + " parts posted to DB")


if __name__ == "__main__":
    manager.run()
