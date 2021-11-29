* [Inicio](#inicio)
* [Documentación API](#api)
* [Ayudas](#ayudas)

* [Tecnologias](#tec)

<div id='inicio' />

# Run Peacth-AC API

Instalar requerimientos
```
pip install -r requirements.txt
```

Se requiere tener una base de datos en mongoDB
```
use peacth-ac
```

Borrar "0001_initial.py"

```
python3 manage.py makemigrations api
python3 manage.py migrate

```

<div id='api' />

# Documentación API

### API root
- https://peacth-ac-backend.rj.r.appspot.com/api/
### ESTIMACIÓN DE DOSIS
#### Calcular dosis semanal [POST]
This method calculate the dose of the patients, but it doesn't save the patient in the database
- patients/get_weekly_dosis/
+ Request (application/JSON)
	+ Body
    ```
    {
    		"code": "T-001",             
    		"sex": "M",                  
    		"initialDate": "2009-11-30", 
    		"initialDose": 0,  # Always 0        
    		"initialINR": 1.1,           
    		"weeklyDoseInRange": 0, # Always 0   
    		"totalDays": 534, 	     
    		"weight": 80.0, 	     
    		"height": 1.68, 	     
    		"imc": 28.3,                
    		"age": 69,                   
    		"genetics": {
				"CYP2C9_2": "*1/*1", 
    			"CYP2C9_3": "*1/*1", 
    			"VKORC1": "A/A"      
    		}
    }
	```
+ Response (application/JSON)
	```
	{
    	"regressionDose": 5.742530690407449,
    	"networkDose": 5.193664073944092
	}
	```
#### Fijar dosis [POST]
This method set the dose of the patients and saves it to the database
- patients/set_dose/
+ Request (application/JSON)
	+ Body
    ```
    {
    		"code": "T-001",             
    		"sex": "M",                  
    		"initialDate": "2009-11-30", 
    		"initialDose": 6.0,   # With the chosen dose       
    		"initialINR": 1.1,           
    		"weeklyDoseInRange": 0,   # Always 0 
    		"totalDays": 534, 	     
    		"weight": 80.0, 	     
    		"height": 1.68, 	     
    		"imc": 28.3,                
    		"age": 69,                   
    		"genetics": {
				"CYP2C9_2": "*1/*1", 
    			"CYP2C9_3": "*1/*1", 
    			"VKORC1": "A/A"      
    		}
    }
	```
+ Response (application/JSON)
	```
	{
		"message" : "Dosis fijada correctamente.",
    	"initialDose": 5.742530690407449
	}
	```

#### Ver un paciente [GET]
This method obtains the info of a pacient with a code
- patients/{code}
+ Response
    ```
    {
    		"code": "T-001",             
    		"sex": "M",                  
    		"initialDate": "2009-11-30", 
    		"initialDose": 6.0,          
    		"initialINR": 1.1,           
    		"weeklyDoseInRange": 10.0,   
    		"totalDays": 534, 	     
    		"weight": 80.0, 	     
    		"height": 1.68, 	     
    		"imc": 28.3,                
    		"age": 69,                   
    		"genetics": {
	    		"CYP2C9_2": "*1/*1", 
    			"CYP2C9_3": "*1/*1", 
    			"VKORC1": "A/A"      
    		}
    }

#### Análisis Genético [GET] (Sujeto a Cambio)
- patients/T-001/genetic_analysis/
+ Response (application JSON)
	```
	{
		"CYP2C9": {
			"CYP2C9*2": "Heterocigoto",
			"CYP2C9*3": "Heterocigoto",
			"resp": "El genotipo del paciente corresponde a un metabolizador intermedio (IM)"
		},
		"VKORC1": {
			"Alelo": "Doble mutado (A/A)",
			"resp": "El genotipo del paciente se relaciona con una menor dosis de Acenocumarol"
		}
	}
	```

#### Perfil del paciente
- patients/{code}/patient_profile/
+ Response (application JSON)
	```
	{
		"clinic": {
			"_id": "60f1ec92e7be8e6f7e378c16",
			"code": "T-003",
			"sex": "M",
			"initialDate": "2009-01-19",
			"initialDose": 12.0,
			"initialINR": 2.0,
			"weeklyDoseInRange": 10.0,
			"totalDays": 94,
			"weight": 0.0,
			"height": 0.0,
			"imc": 0.0,
			"age": 64,
			"genetics": {
				"CYP2C9_2": "*1/*1",
				"CYP2C9_3": "*1/*1",
				"VKORC1": "A/A"
			}
		},
		"genetic": {
			"CYP2C9": {
				"rs1799853": "Ausente",
				"rs1057910": "Ausente",
				"Observaciones": "El genotipo del paciente corresponde a un metabolizador extensivo o silvestre (EM)"
			},
			"VKORC1": {
				"rs9923231": "Doble mutado (A/A)",
				"Observaciones": "El genotipo del paciente se relaciona con una menor dosis de Acenocumarol"
			}
		}
		"historicINR": {
			"dates": [
				"30/11/2009",
				"30/12/2009",
				"30/01/2010",
				"30/03/2010"
			],
			"inrValues": [
				3.4,
				3.7,
				3.2,
				3.0
			],
			"doseValues": [
				0,
				66.0,
				50.0,
				40.0
			]
		}
	}
	```

### Registra visitas
#### Ver todos los controles registrados [GET]
This method allows us to see all the information about medical checks.
- clinical_control/
+ Response (application JSON)
	```
	{ 
		"_id":  "60f1e93f08956a1ceb4ffb5a",  
		"patientCode":  "T-999",  
		"controlDate":  "2009-11-30",  
		"arrivalDose":  0.0,  
		"updatedDose":  9.929399471052776,  
		"arrivalINR":  1.1,  
		"inrInRange":  false
	}
	```
#### Registrar visita [POST]
This method save the information about patient's medical checks 
- clinical_control/register_visit/
+ Request (application/JSON)
	+ Body
		```
		  {   
			  "patientCode":  "T-999",  
			  "controlDate":  "2009-11-30",  
			  "arrivalDose":  0.0,  
			  "updatedDose":  9.929399471052776,  
			  "arrivalINR":  1.1,  
			  "inrInRange":  false  
			}
		```
+ Response (application/JSON)
	```
	{ 
		"message": "Saved Succesfully"
	}
	```
### Actualizar parámetros del algoritmo
#### Actualizar parámetros de forma manual [POST]
This method allow us change the current parameters of the pharmacogenetics algorithm
- LogWTDparameters/set_parametres/set_parametres/
+ Request (application/JSON)
	+ Body
		```
		{  
			"p_0":  3.081,  
			"p_men":  0.167,  
			"p_age":  0.0081,  
			"p_initialINR":  0.055,  
			"p_imc":  0.013, 
			"p_CYP2C9_12":  0.107,  
			"p_CYP2C9_13":  0.323,  
			"p_CYP2C9_33":  0.746,  
			"p_VKORC1_GA":  0.27,  
			"p_VKORC1_AA":  0.701,
			"r_squared": 0.5147  
		}
		```
+ Response (application/JSON)
	```
	{ 
		"message": "Parametres updated Succesfully"
	}
	```
#### Obtener la última actualización de los parámetros [GET]
This method allow us change the current parameters of the pharmacogenetics algorithm
- LogWTDparameters/get_last/get_last
+ Response (application/JSON)
	```
	{
		"_id": "60f1ee881f69782bda74a492",
		"p_0": 3.081,
		"p_men": 0.167,
		"p_age": 0.0081,
		"p_initialINR": 0.055,
		"p_imc": 0.013,
		"p_CYP2C9_12": 0.107,
		"p_CYP2C9_13": 0.323,
		"p_CYP2C9_33": 0.746,
		"p_VKORC1_GA": 0.27,
		"p_VKORC1_AA": 0.701,
		"r_squared": 0.5147
	}
	```
### Regresión lineal [GET]
- LogWTDparameters/multivariable_regression/
+ Response (application/JSON)
	```
	{
		"message": "Los parámetros no se actualizaron debido a que el r2 es menor a la regresión actual",
		"params": {
			"p_0": 4.8519927925716475,
			"p_men": 0.22211275448247525,
			"p_age": -0.012814841488389746,
			"p_initialINR": -0.0784394288974603,
			"p_imc": 0.008287360486787231,
			"p_CYP2C9_12": -0.17796969096743442,
			"p_CYP2C9_13": -0.45815491317751467,
			"p_CYP2C9_33": -1.1406527502812869,
			"p_VKORC1_GA": -0.418752414756341,
			"p_VKORC1_AA": -1.0545597169772143,
			"r_squared": 0.5116452670520679
		}
	}
	```
### Comparación de modelos
- models_analysis/
+ Response (application/JSON)
	```
	[
		{
			"_id": "61a2c16a323df109b65afde1",
			"code": "T-001",
			"network_result": 9.929399471052776,
			"regression_result": 9.107564926147461,
			"network_error": 0.08924350738525391,
			"regression_error": 0.007060052894722446,
			"final_dose": 10.0,
			"is_treatement_done": true
		},
		{
			"_id": "61a2c16b323df109b65afde2",
			"code": "T-002",
			"network_result": 11.289803802260646,
			"regression_result": 8.968988418579102,
			"network_error": 0.5017228656344943,
			"regression_error": 0.3727886776521863,
			"final_dose": 18.0,
			"is_treatement_done": true
		},
		{
			"_id": "61a2c16c323df109b65afde3",
			"code": "T-003",
			"network_result": 6.81141580885468,
			"regression_result": 11.417252540588379,
			"network_error": 0.1417252540588379,
			"regression_error": 0.31885841911453194,
			"final_dose": 10.0,
			"is_treatement_done": true
		},
		...
	]
	```
### Análisis comparativo de la dosis calculada entre genotipos ingresados
+ Parameters
		+ gen (string) : the gene for which information is required
#### Información boxplot [GET]
This method get information needed to plot boxplot
- distributions/boxplot/{gen}
+ Response (application/JSON)
	```
	[
		{
			"label": "A/A",
			"value": [
				-0.75,
				6.0,
				8.0,
				10.5,
				17.25
			]
		},
		{
			"label": "G/A",
			"value": [
				0.5,
				11.0,
				13.25,
				18.0,
				28.5
			]
		},
		{
			"label": "G/G",
			"value": [
				2.0,
				14.0,
				18.0,
				22.0,
				34.0
			]
		}
	]
	```
#### Información distribución [GET]
This methos get information for distribution plots
- distributions/frequency/{gen}
+ Response (application/JSON)
	```
	{
		"labels": [
			"G/A",
			"G/G",
			"A/A"
		],
		"frequency": [
			154,
			84,
			65
		]
	}
	```
### Red neuronal
#### Entrenar Red Neuronal [GET]
This method trains the neural network
- LogWTDparameters/neural_network
+ Response (application/JSON)
	```
	{
		"is_updated" : True,
		"loss": "9.88%",
    	"updated_at_at": "27/10/2021 01:16:50"
    	"message": "Red neuronal actualizada."
	}
	```
#### Obtener último modelo de la Red Neuronal [GET]
This method trains the neural network
- LogWTDparameters/get_last_neural_network/
+ Response (application/JSON)
	```
	{
    	"loss": "9.88%",
    	"created_at": "27/10/2021 01:16:50"
	}
	```
<div id='ayudas' />

#### Enviar email  [POST]
This method send an email to some addressee
- api/send_email/
+ Request (application/JSON)
	+ Body
    ```
    {
    	"email": "example@example.com",
		"totalDosis" : 1,
		"patient" : "T-001"            
    }
	```
+ Response (application/JSON)
	```
	{
    	'response' : 'correo enviado con exito'
    }
	```

<div id='ayudas' />

# Ayudas

- [Documentación de API REST](https://www.django-rest-framework.org/).

- [Conector a base de datos](https://www.djongomapper.com/)

- [Tutorial para conexión a base de datos](https://www.mongodb.com/compatibility/mongodb-and-django)

<div id='peacth' />

# Tecnologías

- Django, MongoDB
- Heroku, MongoDB Atlas Database
- React, PrimeReact, Apexcharts
