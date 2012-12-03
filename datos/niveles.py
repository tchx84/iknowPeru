# Configuracion de niveles
# Formato:
# Prefijo indica una posible parte inicial de la pregunta
# Sufijo indica una posible parte final de la pregunta
# Cada nivel empieza con su nombre entre parentesis rectos
# Variables:
#  - dibujoInicial lista de cosas a dibujar en el mapa al inicio del nivel
#     lineasDepto,capitales
#  - nombreInicial lista de cosas a etiquetar en el mapa al inicio del nivel
#     deptos,capitales
# Cada pregunta es una linea que se inicia con Pregunta =
# sigue el texto de la pregunta (lineas separadas con \)
# sigue el tipo de respuesta y el ID de la respuesta correcta
# finalmente el texto de ayuda si el estudiante se equivoca dos veces
#  tipo de respuesta: 1 depto, 2 ciudad, 3 rio, 4 cuchilla, 5 cerro
#  ID de respuesta: string con el nombre
#  texto de ayuda: string (lineas separadas con \)

from gettext import gettext as _

Prefixes = [
_("We have to look") + "\\" + _("a piece of my ship in"),
_("There's a piece") + "\\" + _("of my ship in"),
_("According to my information") + "\\" +("have to look at"),
_("We have to") + "\\" + _("go up"),
_("A piece of my") + "\\" + _("ship fell into") ]

Suffixes = [
_("Can you point out where it is?"),
_("Where is it?"),
_("Are we going up there?"),
_("you take me?"),
_("Can you show me where it is?") ]

Correct = [
_("Right!"),
_("Great!"),
_("You found it!"),
_("Yes!") ]

Bad = [
_("No, try again"),
_("seems not here"),
_("Keep trying ...") ]

farewell = [
_("Now I can return Farewell to my planet.") + "\\" + _("Thanks for your help!"),
_("My ship is ready.") + "\\" + _("Chau and thanks for helping!"),
_("We did it!") + "\\" + _("I'm Ready to take off.") + "\\" + _("Until next time!") ]

categories = [_("Departments"), _("Capitals"), _("Cities"), _("Waterways"), _("Elevations"), _("Historical Sites")]

dibujoInicial = {}
nombreInicial = {}
Questions = {}

# Departments
dibujoInicial['Departments'] = ["lineasDepto"]
nombreInicial['Departments'] = []
Questions['Departments'] = [
[_("Department") + '\\' + _("of Tumbes"),1,_("Tumbes"),_("Come on, try again")],
[_("Department") + '\\' + _("of Piura"),1,_("Piura"),_("Come on, try again")],
[_("Department") + '\\' + _("of Lambayeque"),1,_("Lambayeque"),_("Come on, try again")],
[_("Department") + '\\' + _("of the Libertad"),1,_("The Libertad"),_("Come on, try again")],
[_("Department") + '\\' + _("of Cajamarca"),1,_("Cajamarca"),_("Come on, try again")],
[_("Department") + '\\' + _("of Amazon"),1,_("Amazon"),_("Come on, try again")],
[_("Department") + '\\' + _("of San Martin"),1,_("San Martin"),_("Come on, try again")],
[_("Department") + '\\' + _("of Loreto"),1,_("Loreto"),_("Come on, try again")],
[_("Department") + '\\' + _("of Ancash"),1,_("Ancash"),_("Come on, try again")],
[_("Department") + '\\' + _("of Huanuco"),1,_("Huanuco"),_("Come on, try again")],
[_("Department") + '\\' + _("of Lima"),1,_("Lima"),_("Come on, try again")],
[_("Department") + '\\' + _("of Pasco"),1,_("Pasco"),_("Come on, try again")],
[_("Department") + '\\' + _("of Junin"),1,_("Junin"),_("Come on, try again")],
[_("Department") + '\\' + _("of Ucayali"),1,_("Ucayali"),_("Come on, try again")],
[_("Department") + '\\' + _("of Ica"),1,_("Ica"),_("Come on, try again")],
[_("Department") + '\\' + _("of Huancavelica"),1,_("Huancavelica"),_("Come on, try again")],
[_("Department") + '\\' + _("of Ayacucho"),1,_("Ayacucho"),_("Come on, try again")],
[_("Department") + '\\' + _("of Apurimac"),1,_("Apurimac"),_("Come on, try again")],
[_("Department") + '\\' + _("of Cusco"),1,_("Cusco"),_("Come on, try again")],
[_("Department") + '\\' + _("of San Martin"),1,_("San Martin"),_("Come on, try again")],
[_("Department") + '\\' + _("of Mother of God"),1,_("Mother of God"),_("Come on, try again")],
[_("Department") + '\\' + _("of Arequipa"),1,_("Arequipa"),_("Come on, try again")],
[_("Department") + '\\' + _("of Puno"),1,_("Puno"),_("Come on, try again")],
[_("Department") + '\\' + _("of Moquegua"),1,_("Moquegua"),_("Come on, try again")],
[_("Department") + '\\' + _("of Tacna"),1,_("Tacna"),_("Come on, try again")] ]

# Departmental Capitals
dibujoInicial['Capitals'] = ["lineasDepto", "capitales"]
nombreInicial['Capitals'] = ["deptos"]
Questions['Capitals'] = [
[_("City") + '\\' + _("of Tumbes"),2,_("Tumbes"),_("Come on, try again")],
[_("City") + '\\' + _("of Piura"),2,_("Piura"),_("Come on, try again")],
[_("City") + '\\' + _("of Chiclayo"),2,_("Chiclayo"),_("Come on, try again")],
[_("City") + '\\' + _("of Trujillo"),2,_("Trujillo"),_("Come on, try again")],
[_("City") + '\\' + _("of Cajamarca"),2,_("Cajamarca"),_("Come on, try again")],
[_("City") + '\\' + _("of Chachapoyas"),2,_("Chachapoyas"),_("Come on, try again")],
[_("City") + '\\' + _("of Moyobamba"),2,_("Moyobamba"),_("Come on, try again")],
[_("City") + '\\' + _("of Huaraz"),2,_("Huaraz"),_("Come on, try again")],
[_("City") + '\\' + _("of Huanuco"),2,_("Huanuco"),_("Come on, try again")],
[_("City") + '\\' + _("of Lima"),2,_("Lima"),_("Come on, try again")],
[_("City") + '\\' + _("of Tumbes"),2,_("Tumbes"),_("Come on, try again")],
[_("City") + '\\' + _("of Hill of Pasco"),2,_("Hill of Pasco"),_("Come on, try again")],
[_("City") + '\\' + _("of Huancayo"),2,_("Huancayo"),_("Come on, try again")],
[_("City") + '\\' + _("of Pucallpa"),2,_("Pucallpa"),_("Come on, try again")],
[_("City") + '\\' + _("of Ica"),2,_("Ica"),_("Come on, try again")],
[_("City") + '\\' + _("of Huancavelica"),2,_("Huancavelica"),_("Come on, try again")],
[_("City") + '\\' + _("of Ayacucho"),2,_("Ayacucho"),_("Come on, try again")],
[_("City") + '\\' + _("of Abancay"),2,_("Abancay"),_("Come on, try again")],
[_("City") + '\\' + _("of Cusco"),2,_("Cusco"),_("Come on, try again")],
[_("City") + '\\' + _("of Puerto Maldonado"),2,_("Puerto Maldonado"),_("Come on, try again")],
[_("City") + '\\' + _("of Arequipa"),2,_("Arequipa"),_("Come on, try again")],
[_("City") + '\\' + _("of Puno"),2,_("Puno"),_("Come on, try again")],
[_("City") + '\\' + _("of Moquegua"),2,_("Moquegua"),_("Come on, try again")],
[_("City") + '\\' + _("of Tacna"),2,_("Tacna"),_("Come on, try again")] ]

# Cities
dibujoInicial['Cities'] = ["lineasDepto", "capitales", "ciudades"]
nombreInicial['Cities'] = ["deptos"]
Questions['Cities'] = [
[_("City") + '\\' + _("of Sullana"),2,_("Sullana"),_("Come on, try again")],
[_("City") + '\\' + _("of Chulucanas"),2,_("Chulucanas"),_("Come on, try again")],
[_("City") + '\\' + _("of Moquegua"),2,_("Moquegua"),_("Come on, try again")],
[_("City") + '\\' + _("of Paita"),2,_("Paita"),_("Come on, try again")],
[_("City") + '\\' + _("of Catacaos"),2,_("Catacaos"),_("Come on, try again")],
[_("City") + '\\' + _("of Talara"),2,_("Talara"),_("Come on, try again")],
[_("City") + '\\' + _("of Barranca"),2,_("Barranca"),_("Come on, try again")],
[_("City") + '\\' + _("of Huancho"),2,_("Huancho"),_("Come on, try again")],
[_("City") + '\\' + _("of Huaral"),2,_("Huaral"),_("Come on, try again")],
[_("City") + '\\' + _("of Chincha"),2,_("Chincha"),_("Come on, try again")],
[_("City") + '\\' + _("of Pisco"),2,_("Pisco"),_("Come on, try again")],
[_("City") + '\\' + _("of Tarapoto"),2,_("Tarapoto"),_("Come on, try again")],
[_("City") + '\\' + _("of Juanjui"),2,_("Juanjui"),_("Come on, try again")],
[_("City") + '\\' + _("of Jaen"),2,_("Jaen"),_("Come on, try again")],
[_("City") + '\\' + _("of Chimbote"),2,_("Chimbote"),_("Come on, try again")],
[_("City") + '\\' + _("of Juliaca"),2,_("Juliaca"),_("Come on, try again")],
[_("City") + '\\' + _("of Ilo"),2,_("Ilo"),_("Come on, try again")],
[_("City") + '\\' + _("of Lambayeque"),2,_("Lambayeque"),_("Come on, try again")],
[_("City") + '\\' + _("of Tingo Maria"),2,_("Tingo Maria"),_("Come on, try again")],
[_("City") + '\\' + _("of Tarma"),2,_("Tarma"),_("Come on, try again")] ]

# Rivers / Waterways

dibujoInicial["Waterways"] = ["lineasDepto", "capitales", "rios"]
nombreInicial["Waterways"] = []
Questions['Waterways'] = [
[_("River Piura"),3,_("River Piura"),_("Come on, try again")],
[_("River Maranon"),3,_("River Maranon"),_("Come on, try again")],
[_("River Amazon"),3,_("River Amazon"),_("Come on, try again")],
[_("River Santa"),3,_("River Santa"),_("Come on, try again")],
[_("River Huallaga"),3,_("River Huallaga"),_("Come on, try again")],
[_("River Ucayali"),3,_("River Ucyali"),_("Come on, try again")],
[_("River Purus"),3,_("River Purus"),_("Come on, try again")],
[_("River of las Piedras"),3,_("River of las Piedras"),_("Come on, try again")],
[_("River Mother of God"),3,_("River Mother of God"),_("Come on, try again")],
[_("River Ica"),3,_("River Ica"),_("Come on, try again")],
[_("River Ocona"),3,_("River Ocona"),_("Come on, try again")],
[_("River Sihuas"),3,_("River Sihuas"),_("Come on, try again")],
[_("River Tambo"),3,_("River Tambo"),_("Come on, try again")],
[_("River Sama"),3,_("River Sama"),_("Come on, try again")],
[_("Pacific Ocean"),3,_("Pacific Ocean"),_("Come on, try again")],
[_("Lake Titicaca"),3,_("Lake Titicaca"),_("Come on, try again")] ]

# Blades
dibujoInicial["Elevations"] = ["cuchillas", "cerros"]
nombreInicial["Elevations"] = []
Questions["Elevations"] = [ [_("The Cordillera Blanca"),4,_("Cordillera Blanca"),_("Come on, try again")] ]

# Historical sites
dibujoInicial["Historical Sites"] = ["lineasDepto","capitales","ciudades"]
nombreInicial["Historical Sites"] = []
Questions["Historical Sites"] = [ [_("The city where Jose") + "\\" + _("San Martin landing"),2,_("Pisco"),_("It is in the department") + "\\" + _("Ica")] ]
