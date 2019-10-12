# -*- coding: utf-8 -*-
import json
from datetime import datetime

import scrapy
from scrapy import FormRequest

from ragoogle.items.odessa import MbuItem
from ragoogle.loaders import StripJoinItemLoader


class OdessaSpider(scrapy.Spider):
    name = "odessa"
    allowed_domains = ["service.ombk.odessa.ua"]
    start_urls = [
        "https://service.ombk.odessa.ua/arcgis/rest/services/GUO/GUO_PASPORT/MapServer/0/query?where=Kadastr2016.DBO.MBU.Data+BETWEEN+timestamp+%271991-08-24+21%3A00%3A00%27+AND+timestamp+%273000-01-01+20%3A59%3A59%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=pjson"]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["number_in_order", "order_no", "order_date", "customer", "obj", "address", "changes",
                               "cancellation", "scan_url", "additional_fields"],
    }

    # API has limit to get only 1000 entities per request
    def start_requests(self):
        # TODO change get by year with better splitting for 1000 entities max
        for year in range(1991, datetime.now().year + 1):
            yield FormRequest(
                "https://service.ombk.odessa.ua/arcgis/rest/services/GUO/GUO_PASPORT/MapServer/0/query",
                dont_filter=True,
                formdata={
                    "where": "Kadastr2016.DBO.MBU.Data BETWEEN timestamp '{}-01-01 00:00:00' AND timestamp '{}-12-31 00:00:00'".format(year, year),
                    "text": "",
                    "objectIds": "",
                    "time": "",
                    "geometry": "",
                    "geometryType": "esriGeometryEnvelope",
                    "inSR": "",
                    "spatialRel": "esriSpatialRelIntersects",
                    "relationParam": "",
                    "outFields": "Kadastr2016.DBO.MBU.OBJECTID, Kadastr2016.DBO.MBU.Data, Kadastr2016.DBO.MBU.KodMBD, Kadastr2016.DBO.MBU.Poverhovist, Kadastr2016.DBO.MBU.Kodadresu, Kadastr2016.DBO.MBU.Naimadresy, Kadastr2016.DBO.MBU.Kodcilpr, Kadastr2016.DBO.MBU.Naimcilpr, Kadastr2016.DBO.MBU.Naimpidkodyfp, Kadastr2016.DBO.MBU.Pidkodobekty, Kadastr2016.DBO.MBU.Nazobekty, Kadastr2016.DBO.MBU.Nazpidkodyob, Kadastr2016.DBO.MBU.Primitka, Kadastr2016.DBO.MBU.Kodfunctpr, Kadastr2016.DBO.MBU.Pidkodfuctpr, Kadastr2016.DBO.MBU.Naimfuncpr, Kadastr2016.DBO.MBU.Kodnamirz, Kadastr2016.DBO.MBU.Naimnamz, Kadastr2016.DBO.MBU.Pravdokdil, Kadastr2016.DBO.MBU.Budobdil, Kadastr2016.DBO.MBU.Kilkvart, Kadastr2016.DBO.MBU.Kilmashmic, Kadastr2016.DBO.MBU.Torgplosh, Kadastr2016.DBO.MBU.Zagplosh, Kadastr2016.DBO.MBU.Ploshzab, Kadastr2016.DBO.MBU.Ploshoz, Kadastr2016.DBO.MBU.Planobm, Kadastr2016.DBO.MBU.Vumohoron, Kadastr2016.DBO.MBU.Kodobbyd, Kadastr2016.DBO.MBU.Kodobksp, Kadastr2016.DBO.MBU.Pidkodobkyl, Kadastr2016.DBO.MBU.Naimkodkylt, Kadastr2016.DBO.MBU.Naimpidkodk, Kadastr2016.DBO.MBU.Kodistareal, Kadastr2016.DBO.MBU.Pidkodisar, Kadastr2016.DBO.MBU.Naimistar, Kadastr2016.DBO.MBU.Naimpidkodisr, Kadastr2016.DBO.MBU.NomerKad, Kadastr2016.DBO.MBU.NomKancel, Kadastr2016.DBO.MBU.NomDoma, Kadastr2016.DBO.MBU.Korpus, Kadastr2016.DBO.MBU.Kvart, Kadastr2016.DBO.MBU.PlosZemDil, Kadastr2016.DBO.MBU.MaxVidZab, Kadastr2016.DBO.MBU.Zamovnuk_MBO, Kadastr2016.DBO.MBU.Naim_MBD, Kadastr2016.DBO.MBU.Prumitku_1, Kadastr2016.DBO.MBU.Status, Kadastr2016.DBO.MBU.Zam_MBO, Kadastr2016.DBO.MBU.GlobalID, Kadastr2016.DBO.MBU.Link_1, Kadastr2016.DBO.MBU.Link_2, Kadastr2016.DBO.MBU.Kilkvart_, Kadastr2016.DBO.MBU.Data_nakaz, Kadastr2016.DBO.MBU.Nom_nakaz, Kadastr2016.DBO.MBU.Zmini, Kadastr2016.DBO.MBU.Skasuvannia, Kadastr2016.DBO.MBU.S, Kadastr2016.DBO.Rej_Vul.KOD_KLS, Kadastr2016.DBO.Rej_Vul.ID_MSB_OBJ, Kadastr2016.DBO.Rej_Vul.NAZVA_UKR, Kadastr2016.DBO.Rej_Vul.NAZVA_ROS, Kadastr2016.DBO.Rej_Vul.NAZVA_LAT, Kadastr2016.DBO.Rej_Vul.KOATUU, Kadastr2016.DBO.Rej_Vul.RuleID, Kadastr2016.DBO.Rej_Vul.Prymitka, Kadastr2016.DBO.Rej_Vul.NomerDocument, Kadastr2016.DBO.Rej_Vul.DataDocument, Kadastr2016.DBO.Rej_Vul.KOD_KAT_UKR_SK, Kadastr2016.DBO.Rej_Vul.NAZVA_ANH, Kadastr2016.DBO.Rej_Vul.KOD_KAT_ROS_SK, Kadastr2016.DBO.Rej_Vul.KOD_KAT_ANH_SK, Kadastr2016.DBO.Rej_Vul.KOD_KAT_LAT_SK, Kadastr2016.DBO.Rej_Vul.KOD_KAT_ROS, Kadastr2016.DBO.Rej_Vul.KOD_KAT_UKR, Kadastr2016.DBO.Rej_Vul.KOD_KAT_LAT, Kadastr2016.DBO.Rej_Vul.KOD_KAT_ANH, Kadastr2016.DBO.Rej_Vul.GlobalID",
                    "returnGeometry": "false",
                    "returnTrueCurves": "false",
                    "maxAllowableOffset": "100000",
                    "geometryPrecision": "",
                    "outSR": "",
                    "having": "",
                    "returnIdsOnly": "false",
                    "returnCountOnly": "false",
                    "orderByFields": "",
                    "groupByFieldsForStatistics": "",
                    "outStatistics": "",
                    "returnZ": "false",
                    "returnM": "false",
                    "gdbVersion": "",
                    "historicMoment": "",
                    "returnDistinctValues": "false",
                    "resultOffset": "",
                    "resultRecordCount": "",
                    "queryByDistance": "",
                    "returnExtentOnly": "false",
                    "datumTransformation": "",
                    "parameterValues": "",
                    "rangeValues": "",
                    "quantizationParameters": "",
                    "featureEncoding": "esriDefault",
                    "f": "pjson"
                }
            )

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for attributes in jsonresponse['features']:
            self.logger.debug("parse row : {}".format(attributes))
            attributes = attributes['attributes']
            l = StripJoinItemLoader(item=MbuItem())
            l.add_value("number_in_order", str(attributes['Kadastr2016.DBO.MBU.OBJECTID']))
            l.add_value("order_no", attributes['Kadastr2016.DBO.MBU.NomKancel'] if attributes['Kadastr2016.DBO.MBU.NomKancel'] else '-')
            l.add_value("order_date",
                        str(datetime.fromtimestamp(attributes['Kadastr2016.DBO.MBU.Data'] / 1000).date()) if attributes[
                            'Kadastr2016.DBO.MBU.Data'] else None)
            l.add_value("customer", attributes['Kadastr2016.DBO.MBU.Zamovnuk_MBO'])
            l.add_value("obj", attributes['Kadastr2016.DBO.MBU.Nazobekty'])
            l.add_value("address", self.get_address(attributes))
            l.add_value("changes", attributes['Kadastr2016.DBO.MBU.Zmini'])
            l.add_value("cancellation", attributes['Kadastr2016.DBO.MBU.Skasuvannia'])

            # all original fields to be used later
            additional_fields = dict([[item[len('Kadastr2016.DBO.'):],attributes[item]] for item in attributes.keys()])

            l.add_value('additional_fields', json.dumps(additional_fields, ensure_ascii=False))

            scan_urls = []
            if attributes['Kadastr2016.DBO.MBU.Link_1']:
                scan_urls.append(response.urljoin(attributes['Kadastr2016.DBO.MBU.Link_1']))

            if attributes['Kadastr2016.DBO.MBU.Link_2']:
                scan_urls.append(response.urljoin(attributes['Kadastr2016.DBO.MBU.Link_2']))

            if scan_urls:
                l.add_value("scan_url", ",".join(scan_urls))

            yield l.load_item()

    def get_address(self, attributes):
        address = ''
        street = attributes['Kadastr2016.DBO.Rej_Vul.NAZVA_UKR']
        house_number = attributes['Kadastr2016.DBO.MBU.NomDoma']
        building_part = attributes['Kadastr2016.DBO.MBU.Korpus']
        apartment_number = attributes['Kadastr2016.DBO.MBU.Kvart']

        address = address + street if street else address

        if house_number:
            address = address + ', буд. ' + house_number
            address = address + ', корпус ' + building_part if building_part else address
            address = address + ', кв. ' + apartment_number if apartment_number else address

        return address
