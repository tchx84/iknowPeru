# Configuracion de exploraciones
# Formato:
# Cada nivel empieza con su nombre entre parentesis rectos
# Variables:
#  - dibujoInicial lista de cosas a dibujar en el mapa al inicio del nivel
#     lineasDepto,capitales
#  - nombreInicial lista de cosas a etiquetar en el mapa al inicio del nivel
#     deptos,capitales
#  - elementosActivos lista de cosas que se activan al cliquear

from gettext import gettext as _

CONFIGURATION = {
_("Explore departaments"): """dibujoInicial = lineasDepto
nombreInicial =
elementosActivos = deptos""",
_("Explore capitals"): """dibujoInicial = lineasDepto, capitales
nombreInicial = deptos
elementosActivos = capitales""",
_("Explore cities"): """dibujoInicial = lineasDepto, capitales, ciudades
nombreInicial = deptos
elementosActivos = capitales, ciudades""",
_("Explore watershowers"): """dibujoInicial = rios
nombreInicial =
elementosActivos = rios""",
_("Explore elevations"): """dibujoInicial = cuchillas, cerros
nombreInicial =
elementosActivos = cuchillas, cerros"""
}
