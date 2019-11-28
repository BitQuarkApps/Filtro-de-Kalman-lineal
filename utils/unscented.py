class Unscented:
	"""
	Clase que contiene los métodos que la extensión Unscented del
	filtro de Kalman requiere
	"""
    def __init__(self):
		print("=== Filtro de Kalman Unscented ===")
	
	def obtener_puntos_sigma(self, X0, Px):
		
