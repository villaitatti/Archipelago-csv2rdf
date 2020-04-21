import pandas as pd
import numpy as np
import string
import random
import os

from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD

# Utility methods
def _id(stringLength=8):

    chars = string.ascii_uppercase + string.digits
    chars = chars.replace('I','')
    chars = chars.replace('O','')
    chars = chars.replace('1','')
    chars = chars.replace('0','')

    return ''.join(random.choice(chars) for i in range(stringLength))

input_file = os.path.join('csv','bw_buildings.csv')
output_file = os.path.join('rdf','bw_buildings.ttl')

df = pd.read_csv(input_file, sep=';')


# Namespaces

crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')


# URIs
URI_base = 'https://archipelago.itatti.harvard.edu/resource/'

# Keys
#input
key_csv_bw = 'BW_ID'
key_csv_name = 'Name'
key_csv_island = 'IslandName'
key_csv_date_start = 'Start_Earliest'
key_csv_date_end = 'End_Latest'
key_csv_func = 'Function'
key_csv_func_start = 'Start_Function'
key_csv_func_end = 'End_Function'
key_csv_use = 'Use'
key_csv_use_start = 'Start_Use'
key_csv_use_end = 'End_Function'
key_csv_typo = 'Typology'
key_csv_typo_start = 'Start_Typology'
key_csv_typo_end = 'End_Typology'
key_csv_h = 'Height'
key_csv_material = 'Material'
key_csv_architect = 'Architect'
key_csv_owner = 'Owner'
key_csv_owner_start = 'Start_Owner'
key_csv_owner_end = 'End_Owner'
key_csv_tenant = 'Tenant'
key_csv_tenant_start = 'Start_Tenant'
key_csv_tenant_end = 'End_Tenant'
key_csv_p = 'SHP_Lenght'
key_csv_a = 'SHP_Area'

key_wkt = 'WKT'

key_uri_bw = 'built_work'
key_uri_id = 'identifier'
key_uri_loc = 'location'
key_uri_type = 'type'
key_uri_func = 'function'
key_uri_use_start = 'use_start'
key_uri_use_end = 'use_end'
key_uri_typo_start = 'typology_start'
key_uri_typo_end = 'typology_end'
key_uri_construction = 'construction'
key_uri_destruction = 'destruction'
key_uri_time = 'timespan'
key_uri_pref_name = 'preferred_name'

key_uri_measurement = 'measurement'
key_uri_dimension = 'dimension'
key_uri_measurement_unit = 'measurement_unit'
key_uri_material = 'material'
key_uri_architect = 'architect'

key_uri_owner = 'owner'
key_uri_acquisition = 'acquisition'
key_uri_tenant = 'tenant'

key_uri_type_island = 'Island'
key_uri_type_bw = 'Built Work'

key_cat_function = 'Function'
key_cat_use_start = 'Start Use'
key_cat_use_end = 'End Use'
key_cat_typo_start = 'Start Typology'
key_cat_typo_end = 'End Typology'
key_cat_h = 'Height'
key_cat_mt = 'Meters(??)'
key_cat_material = 'Material'
key_cat_architect = 'Architect'
ket_cat_owner = 'Owner'
key_cat_tenant = 'Tenant'

def _add_bw(g, data):

    g.namespace_manager.bind('crm', crm, override = True, replace=True)

    E52_Time = 'E52_Time-span'
    p4_has_time = 'p4_has_time-span'

    # URIs
    bw_uri = f'{URI_base}{key_uri_bw}/{_id()}'
    bw_id_uri = f'{bw_uri}/{key_uri_id}/{_id()}'
    bw_type_uri = f'{bw_uri}/{key_uri_type}/{_id()}'

    bw_name_uri = f'{bw_uri}/{key_uri_pref_name}/{_id()}'
    bw_name_type_uri = f'{bw_name_uri}/{key_uri_type}/{_id()}'

    bw_loc_uri = f'{URI_base}{key_uri_type_island}/{_id()}'
    bw_loc_id_uri = f'{bw_loc_uri}/{key_uri_id}/{_id()}'

    bw_prod_uri = f'{bw_uri}/{key_uri_construction}/{_id()}'
    bw_prod_type_uri = f'{bw_prod_uri}/{key_uri_type}/{_id()}'
    bw_prod_ts_uri = f'{bw_prod_uri}/{key_uri_time}/{_id()}'

    bw_desc_uri = f'{bw_uri}/{key_uri_destruction}/{_id()}'
    bw_desc_ts_uri = f'{bw_desc_uri}/{key_uri_time}/{_id()}'

    # function uris
    bw_func_uri = f'{bw_uri}/{key_uri_func}/{_id()}'
    bw_func_type_uri = f'{bw_func_uri}/{key_uri_type}/{_id()}'
    bw_func_time_uri = f'{bw_func_uri}/{key_uri_time}/{_id()}'

    # use uris
    bw_use_start_uri = f'{bw_uri}/{key_uri_use_start}/{_id()}'
    bw_use_end_uri = f'{bw_uri}/{key_uri_use_end}/{_id()}'
    bw_use_start_type_uri = f'{bw_use_start_uri}/{key_uri_type}/{_id()}'
    bw_use_end_type_uri = f'{bw_use_end_uri}/{key_uri_type}/{_id()}'
    bw_use_start_time_uri = f'{bw_use_start_uri}/{key_uri_time}/{_id()}'
    bw_use_end_time_uri = f'{bw_use_end_uri}/{key_uri_type}/{_id()}'

    # typology uris
    bw_typo_start_uri = f'{bw_uri}/{key_uri_typo_start}/{_id()}'
    bw_typo_end_uri = f'{bw_uri}/{key_uri_typo_end}/{_id()}'
    bw_typo_start_type_uri = f'{bw_typo_start_uri}/{key_uri_type}/{_id()}'
    bw_typo_end_type_uri = f'{bw_typo_end_uri}/{key_uri_type}/{_id()}'
    bw_typo_start_time_uri = f'{bw_typo_start_uri}/{key_uri_time}/{_id()}'
    bw_typo_end_time_uri = f'{bw_typo_end_uri}/{key_uri_time}/{_id()}'

    # height
    bw_height_measurement_uri = f'{bw_uri}/{key_uri_measurement}/{_id()}'
    bw_height_dimension_uri = f'{bw_height_measurement_uri}/{key_uri_dimension}/{_id()}'
    bw_height_dimension_unit_uri = f'{bw_height_dimension_uri}/{key_uri_measurement_unit}/{_id()}'
    bw_height_dimension_type_uri = f'{bw_height_dimension_uri}/{key_uri_type}/{_id()}'

    # architect
    bw_prod_arch_role_uri = f'{bw_prod_uri}/{key_uri_architect}_role/{_id()}'
    bw_prod_arch_type_uri = f'{bw_prod_arch_role_uri}/{key_uri_type}/{_id()}'
    bw_prod_arch_uri = f'{bw_prod_arch_role_uri}/{key_uri_architect}/{_id()}'

    # owner 
    bw_owner_acquisition_uri = f'{bw_uri}/{key_uri_acquisition}/{_id()}'
    bw_owner_acquisition_time_uri = f'{bw_owner_acquisition_uri}/{key_uri_time}'

    # Nodes
    bw_node = URIRef(bw_uri)
    bw_id_node = URIRef(bw_id_uri)
    bw_type_uri = URIRef(bw_type_uri)

    bw_name_node = URIRef(bw_name_uri)
    bw_name_type_node = URIRef(bw_name_type_uri)

    bw_loc_node = URIRef(bw_loc_uri)
    bw_loc_id_node = URIRef(bw_loc_id_uri)

    bw_prod_node = URIRef(bw_prod_uri)
    bw_prod_type_node = URIRef(bw_prod_type_uri)
    bw_prod_ts_node = URIRef(bw_prod_ts_uri)

    bw_desc_node = URIRef(bw_desc_uri)
    bw_desc_ts_node = URIRef(bw_desc_ts_uri)

    bw_func_node = URIRef(bw_func_uri)
    bw_func_type_node = URIRef(bw_func_type_uri)
    bw_func_ts_node = URIRef(bw_func_time_uri)

    bw_use_start_node = URIRef(bw_use_start_uri)
    bw_use_end_node = URIRef(bw_use_end_uri)
    bw_use_start_type_node = URIRef(bw_use_start_type_uri)
    bw_use_end_type_node = URIRef(bw_use_end_type_uri)
    bw_use_start_time_node = URIRef(bw_use_start_time_uri)
    bw_use_end_time_node = URIRef(bw_use_end_time_uri)

    bw_typo_start_node = URIRef(bw_typo_start_uri)
    bw_typo_end_node = URIRef(bw_typo_end_uri)
    bw_typo_start_type_node = URIRef(bw_typo_start_type_uri)
    bw_typo_end_type_node = URIRef(bw_typo_end_type_uri)
    bw_typo_start_time_node = URIRef(bw_typo_start_time_uri)
    bw_typo_end_time_node = URIRef(bw_typo_end_time_uri)

    bw_height_measurement_node = URIRef(bw_height_measurement_uri)
    bw_height_dimension_node = URIRef(bw_height_dimension_uri)
    bw_height_dimension_unit_node = URIRef(bw_height_dimension_unit_uri)
    bw_height_dimension_type_node = URIRef(bw_height_dimension_type_uri)

    bw_prod_arch_role_node = URIRef(bw_prod_arch_role_uri)
    bw_prod_arch_node = URIRef(bw_prod_arch_uri)
    bw_prod_arch_type_node = URIRef(bw_prod_arch_type_uri)

    # bw
    g.add( (bw_node, RDF.type, crm['E22_Man-made_Object']) )

    # bw type
    g.add( (bw_node, crm.P2_has_type, bw_type_uri) )
    g.add( (bw_type_uri, RDF.type, crm.E55_Type) )
    g.add( (bw_type_uri, RDFS.label, Literal(key_uri_type_bw, datatype=XSD.string)) )

    # bw name
    g.add( (bw_node, crm.p1_is_identified_by, bw_name_node))
    g.add( (bw_name_node, RDF.type, crm.E41_Appellation) )
    g.add( (bw_name_node, RDFS.label, Literal(data[key_csv_name],datatype=XSD.string)) )

    g.add( (bw_name_node, crm.p2_has_type, bw_name_type_node) )
    g.add( (bw_name_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_name_type_node, RDFS.label, Literal('Preferred Name', datatype=XSD.string)) )

    # bw id
    g.add( (bw_node, crm.p1_is_identified_by, bw_id_node))
    g.add( (bw_id_node, RDF.type, crm.E42_Identifier) )
    g.add( (bw_id_node, RDFS.label, Literal(data[key_csv_bw], datatype=XSD.string)))

    # bw location
    g.add( (bw_loc_node, RDF.type, crm.E53_Place) )

    g.add( (bw_node, crm.P53_has_former_or_current_location, bw_loc_node))
    g.add( (bw_loc_node, crm.p1_is_identified_by, bw_loc_id_node))

    g.add( (bw_loc_id_node, RDF.type, crm.E41_Appellation) )
    g.add( (bw_loc_id_node, RDFS.label, Literal(data[key_csv_island],datatype=XSD.string)))

    # bw production
    g.add( (bw_prod_node, RDF.type, crm.E12_Production) )

    g.add( (bw_node, crm.p108i_was_produced_by, bw_prod_node) )
    g.add( (bw_prod_node, crm.p2_has_type, bw_prod_type_node))

    g.add( (bw_prod_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_prod_type_node, RDFS.label, Literal('Construction', datatype=XSD.string)))

    # bw production timespan
    g.add( (bw_prod_ts_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_prod_ts_node, crm.p82a_begin_of_the_begin, Literal(data[key_csv_date_start],datatype=XSD.date)))
    g.add( (bw_prod_node, crm[p4_has_time], bw_prod_ts_node))

    # bw destruction
    g.add( (bw_desc_node, RDF.type, crm.E6_Destruction) )
    g.add( (bw_node, crm.p13i_was_destroyed_by, bw_desc_node) )

    # bw destruction timespan
    g.add( (bw_desc_ts_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_desc_ts_node, crm.p82b_end_of_the_end, Literal(data[key_csv_date_end],datatype=XSD.date)))
    g.add( (bw_desc_node, crm[p4_has_time], bw_desc_ts_node))

    # bw function
    g.add( (bw_node, crm.p12_was_present_at, bw_func_node) )
    g.add( (bw_func_node, RDF.type, crm.E5_Event) )
    g.add( (bw_func_node, RDFS.label, Literal(data[key_csv_func], datatype=XSD.string)) )

    g.add( (bw_func_node, crm.p2_has_type, bw_func_type_node) )
    g.add( (bw_func_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_func_type_node, RDFS.label, Literal(key_cat_function, datatype=XSD.string)) )

    g.add( (bw_func_node, crm[p4_has_time], bw_func_ts_node) )
    g.add( (bw_func_ts_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_func_ts_node, crm.p82a_begin_of_the_begin, Literal(data[key_csv_func_start], datatype=XSD.date)) )
    g.add( (bw_func_ts_node, crm.p82b_end_of_the_end, Literal(data[key_csv_func_end], datatype=XSD.date)) )

    # bw use start
    g.add( (bw_node, crm.p12_was_present_at, bw_use_start_node) )
    g.add( (bw_use_start_node, RDF.type, crm.E5_Event) )
    g.add( (bw_use_start_node, RDFS.label, Literal(data[key_csv_use], datatype=XSD.string)) )
    g.add( (bw_use_start_node, crm.p2_has_type, bw_use_start_type_node) )
    g.add( (bw_use_start_node, crm[p4_has_time], bw_use_start_time_node) )
    g.add( (bw_use_start_node, crm.p134i_was_continued_by, bw_use_end_node) )

    g.add( (bw_use_start_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_use_start_type_node, RDFS.label, Literal(key_cat_use_start, datatype=XSD.date)) )

    g.add( (bw_use_start_time_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_use_start_time_node, crm.p82a_begin_of_the_begin, Literal(data[key_csv_use_start], datatype=XSD.date)) )

    # bw use end
    g.add( (bw_node, crm.p12_was_present_at, bw_use_end_node) )
    g.add( (bw_use_end_node, RDF.type, crm.E5_Event) )
    g.add( (bw_use_end_node, RDFS.label, Literal(data[key_csv_use], datatype=XSD.string)) )
    g.add( (bw_use_end_node, crm.p2_has_type, bw_use_end_type_node) )
    g.add( (bw_use_end_node, crm[p4_has_time], bw_use_end_time_node) )

    g.add( (bw_use_end_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_use_end_type_node, RDFS.label, Literal(key_cat_use_end, datatype=XSD.date)) )

    g.add( (bw_use_end_time_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_use_end_time_node, crm.p82b_end_of_the_end, Literal(data[key_csv_use_end], datatype=XSD.date)) )

    # bw typology start
    g.add( (bw_node, crm.p12_was_present_at, bw_typo_start_node) )
    g.add( (bw_typo_start_node, RDF.type, crm.E5_Event) )
    g.add( (bw_typo_start_node, RDFS.label, Literal(data[key_csv_typo], datatype=XSD.string)) )
    g.add( (bw_typo_start_node, crm.p2_has_type, bw_typo_start_type_node) )
    g.add( (bw_typo_start_node, crm[p4_has_time], bw_typo_start_time_node) )

    g.add( (bw_typo_start_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_typo_start_type_node, RDFS.label, Literal(key_cat_typo_start, datatype=XSD.string)) )

    g.add( (bw_typo_start_time_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_typo_start_time_node, crm.p82a_begin_of_the_begin, Literal(data[key_csv_typo_start], datatype=XSD.date)) )

    # bw typology end
    g.add( (bw_node, crm.p12_was_present_at, bw_typo_end_node) )
    g.add( (bw_typo_end_node, RDF.type, crm.E5_Event) )
    g.add( (bw_typo_end_node, RDFS.label, Literal(data[key_csv_typo], datatype=XSD.string)) )
    g.add( (bw_typo_end_node, crm.p2_has_type, bw_typo_end_type_node) )
    g.add( (bw_typo_end_node, crm[p4_has_time], bw_typo_end_time_node) )

    g.add( (bw_typo_end_type_node, RDF.type, crm.E55_Type) )
    g.add( (bw_typo_end_type_node, RDFS.label, Literal(key_cat_typo_end, datatype=XSD.string)) )

    g.add( (bw_typo_end_time_node, RDF.type, crm[E52_Time]) )
    g.add( (bw_typo_end_time_node, crm.p82b_end_of_the_end, Literal(data[key_csv_typo_end], datatype=XSD.date)) )

    # bw height
    if not pd.isnull(data[key_csv_h]):

        g.add( (bw_node, crm.p39_was_measured_by, bw_height_measurement_node) )

        g.add( (bw_height_measurement_node, RDF.type, crm.E16_Measurement) )
        g.add( (bw_height_measurement_node, crm.p40_observed_dimension, bw_height_dimension_node) )

        g.add( (bw_height_dimension_node, RDF.type, crm.E54_Dimension) )
        g.add( (bw_height_dimension_node, crm.p90_has_value, Literal(data[key_csv_h], datatype=XSD.decimal)) )
        g.add( (bw_height_dimension_node, crm.p2_has_type, bw_height_dimension_type_node) )
        g.add( (bw_height_dimension_node, crm.p91_has_unit, bw_height_dimension_unit_node) )

        g.add( (bw_height_dimension_type_node, RDF.type, crm.E55_type) )
        g.add( (bw_height_dimension_type_node, RDFS.label, Literal(key_cat_h, datatype=XSD.string)) )

        g.add( (bw_height_dimension_unit_node, RDF.type, crm.E58_Measurement_Unit) )
        g.add( (bw_height_dimension_unit_node, RDFS.label, Literal(key_cat_mt, datatype=XSD.string)) )

    # bw material
    if not pd.isnull(data[key_csv_material]):

        for material in data[key_csv_material].split(' ; '):
            bw_material_uri = f'{bw_uri}/{key_uri_material}/{_id()}'
            bw_material_node = URIRef(bw_material_uri)

            g.add( (bw_node, crm.p45_consist_of, bw_material_node) )
            g.add( (bw_material_node, RDF.type, crm.E57_Material) )
            g.add( (bw_material_node, RDFS.label, Literal(material, datatype=XSD.string)) )

    # bw architect
    if not pd.isnull(data[key_csv_architect]):

        g.add( (bw_prod_arch_role_node, RDF.type, crm.pc14_carried_out_by) )
        g.add( (bw_prod_arch_role_node, crm.p01_has_domain, bw_prod_node) )
        g.add( (bw_prod_arch_role_node, crm.p02_has_range, bw_prod_arch_node) )
        g.add( (bw_prod_arch_role_node, crm.pc14_in_the_role_of, bw_prod_arch_role_node) )

        g.add( (bw_prod_arch_type_node, RDF.type, crm.E55_Type) )
        g.add( (bw_prod_arch_type_node, RDFS.label, Literal(key_cat_architect, datatype=XSD.string)) )

        g.add( (bw_prod_arch_node, RDF.type, crm.E21_Person) )
        g.add( (bw_prod_arch_node, RDFS.label, Literal(data[key_csv_architect], datatype=XSD.string)) )

    #owner
    if not pd.isnull(data[key_csv_owner]):
        return


    return g


for key, bw in df.iterrows():

    g = Graph()

    g = _add_bw(g, bw)

    g.serialize(destination=output_file, format='turtle')

    break
