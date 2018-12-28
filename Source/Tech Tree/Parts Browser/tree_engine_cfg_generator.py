import part_data
from string import Template

tree_engine_header = """
//*********************************************************************************************
//  ENGINE_CONFIG TECH TREE PLACEMENT
//	This places the Engine_Config parts and creates the upgrade icons for the tree
//  
//	DO NOT EDIT THIS FILE DIRECTLY!!!
//	This file is generated using the RP-0 Parts Browser
//
//*********************************************************************************************

@PART[*]:HAS[@MODULE[ModuleEngineConfigs]]:BEFORE[RealismOverhaulEnginesPost]
{
        @MODULE[ModuleEngineConfigs],*
        {
"""

tree_engine_mid = """
        }
}
"""

module_engine_config_template = Template("""
            @CONFIG[${name}]
            {
                %techRequired = ${technology}
                %cost = ${cost}${optional_attributes}
            }
""")

part_upgrade_config_template = Template("""
PARTUPGRADE
{
        name = RFUpgrade_${name}
        partIcon = RO-H1-RS27 // FIXME Once we get dedicated model
        techRequired = ${technology}
        entryCost = 0
        cost = 0      
        title = ${engine_config} Engine Upgrade: ${name} Config
        basicInfo = Engine Performance Upgrade
        manufacturer = Engine Upgrade
        deleteme = 1
        description = The ${engine_config} Engine now supports the ${name} configuration for increased performance. Unlock it in the VAB/SPH through the engine configs interface.\\n\\n${description}
}
""")

def generate_engine_tree(parts):
    engine_configs = ""
    part_upgrades = ""
    for part in parts:
        if "Engine_Config" == part["mod"] and not part['orphan']:
            engine_configs += generate_engine_config(part)
            if 'upgrade' in part and part['upgrade'] is True:
                part_upgrades += generate_part_upgrade_config(part)
    text_file = open("output/TREE-Engines.cfg", "w", newline='\n')
    text_file.write(tree_engine_header)
    text_file.write(engine_configs)
    text_file.write(tree_engine_mid)
    text_file.write(part_upgrades)
    text_file.close()
        
def generate_engine_config(part):
    optional_attributes = ""
    if 'description' in part and len(part['description']) > 0:
        optional_attributes += """
                %description = """ + part['description']
    if 'upgrade' in part and part['upgrade'] is True:
        optional_attributes += """
                *@PARTUPGRADE[RFUpgrade_""" + part['name'] + """]/deleteme -= 1"""
    return module_engine_config_template.substitute(name=part['name'], technology=part['technology'], cost=part['cost'], optional_attributes=optional_attributes)

def generate_part_upgrade_config(part):
    return part_upgrade_config_template.substitute(name=part['name'], technology=part['technology'], engine_config=part['engine_config'], description=part['description'])
    
