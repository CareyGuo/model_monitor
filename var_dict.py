# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 09:38:50 2019

@author: dell-3450-i3
"""
province=[
"JAWA_BARAT","DKI_JAKARTA","JAWA_TIMUR","PROVINSI_JAWA_BARAT","PROVINSI_DKI_JAKARTA",
"BANTEN","JAWA_TENGAH","PROVINSI_JAWA_TIMUR","PROVINSI_BANTEN","SUMATERA_UTARA","PROVINSI_JAWA_TENGAH",
"SUMATERA_SELATAN","SULAWESI_SELATAN","BALI","KALIMANTAN_TIMUR","RIAU","SULAWESI_UTARA","SUMATERA_BARAT",
"LAMPUNG","KEPULAUAN_RIAU"
]
city=[
"JAKARTA_TIMUR","JAKARTA_SELATAN","JAKARTA_BARAT","KOTA_BEKASI","KOTA_SURABAYA","KOTA_BANDUNG",
"JAKARTA_UTARA","KOTA_DEPOK","KOTA_TANGERANG","KABUPATEN_BOGOR","JAKARTA_PUSAT","KOTA_TANGERANG_SELATAN",
"KABUPATEN_BEKASI","KABUPATEN_BANDUNG","KABUPATEN_TANGERANG","KOTA_SEMARANG","KOTA_BOGOR","KOTA_MEDAN",
"KABUPATEN_SIDOARJO","KABUPATEN_KARAWANG","KOTA_PALEMBANG","KABUPATEN_SUKABUMI","KABUPATEN_GARUT",
"KOTA_MAKASSAR","KOTA_BATAM"]
acard_var_dict={

'product':{
        'value':['ISS001','ISS002', 'ISS003', 'ISS004', 'ISS005', 'ISS006',],
        'convert':False,
        } ,    
'married':{ 
        'value':['M001', 'M001','M003',],
        'convert':False,
        }, 
'education':{
        'value':['ED001', 'ED002', 'ED003', 'ED004', 'ED005', 'ED006'],        	
        'convert':False,
        },         
'settle_length':{
        'value':['LT001', 'LT002', 'LT003', 'LT004', 'LT005', 'LT006'],
        'convert':False,
        },      
'house_status':{
        'value':['H001', 'H002', 'H003', 'H004'],
        'convert':False,
        },     
'home_address_province':{
        'value':province,
        'convert':False,
        },
'home_address_city':{
        'value':city,
        'convert':False,
        },
'income':{
        'value':['MS001', 'MS002', 'MS003', 'MS004'],
        'convert':False,
        },
'home_type':{
        'value':['H001', 'H002', 'H003', 'H004'],
        'convert':False,
        },
'work_salary':{
        'value':['MS001', 'MS002', 'MS003', 'MS004'],
        'convert':False,
        },
'client_type':{
        'value':['1001', '1002', '1003'],
        'convert':False,
        },
'contact1_type':{
        'value':['3001', '3002','3003','3004','3005','3006','3007','3008'],
        'convert':True,
        },        
'contact2_type':{
        'value':['3001', '3002','3003','3004','3005','3006','3007','3008'],
        'convert':True,
        },        
'contact3_type':{
        'value':['3001', '3002','3003','3004','3005','3006','3007','3008'],
        'convert':True,
        },
'issue_province':{
        'value':province,
        'convert':False,
        }, 
'issue_city':{
        'value':city,
        'convert':False,
        }, 
'industry':{
        'value':['I001', 'I002', 'I003', 'I004', 'I005', 'I006', 'I007', 'I008', 'I009', 'I010', 'I011', 'I012'],
        'convert':False,
        },   
'work_length':{
        'value':['WL001', 'WL002', 'WL003', 'WL004', 'WL005', 'WL006'],
        'convert':False,
        }, 
'work_province':{
        'value':province,
        'convert':False,
        }, 
'work_city':{
        'value':city,
        'convert':False,
        }, 
'ocr_faith':{
        'value':['ISLAM', 'KRISTEN', 'KATHOLIK', 'BUDHA', 'HINDU'],
        'convert':False,
        }, 
'izi_phone_verify':{
        'value':['true', 'false'],
        'convert':False,
        }, 
'izi_phone_duration':{
        'value':['3-4month','4-5month','5-6month','6-8month','8-10month','10-12month','12month' ],
        'convert':False,
        }, 
'has_whatsapp':{
	      'value':['Adalah','Apakah'],
        'convert':False,	
},   
'service_name' :{
        'value':['S_TELKOMSEL', 'S_XL_Axiata', 'S_Indosat_Ooredoo', 'S_3', 'S_IND_TELKOMSEL','S_XL','S_Smartfren','S_XL_4G_LTE' ],
        'convert':False,
        } ,
'phone_brand':{
        'value':['SAMSUNG', 'OPPO', 'XIAOMI', 'VIVO', 'ASUS','REALME','LENOVO','HUAWEI','SONY'],
        'convert':False,
        }, 
'apply_channel':{	
	      'value':['BD001', 'BD002', 'BD003', 'BD004', 'BD005'],
        'convert':False,
				} ,     
'work_industry':{
        'value':['W001', 'W002', 'W003', 'W004', 'W005', 'W006', 'W007','W008', 'W009', 'W010', 'W011', 'W012', 'W013', 'W014'],
        'convert':False,
        } ,
'fraud2_level':{
        'value':['C', 'S', 'H'],
        'convert':False,	
        },  
'izi_whatsapp_result':{
        'value':['yes', 'no', 'checking'],
        'convert':False,	
        },
'fraud1_level':{
        'value':['C', 'S', 'H'],
        'convert':False,	
        },          
'channel':{
        'value':['BD001', 'BD002', 'BD005'],
        'convert':False,	
        }, 
'product_property':{
        'value':['TYPE001', 'TYPE002', 'TYPE003'],
        'convert':False,	
        }, 
} 

