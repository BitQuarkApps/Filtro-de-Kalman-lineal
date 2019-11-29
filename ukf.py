from utils.unscented import Unscented
import numpy as np

if __name__ == '__main__':
	kf = Unscented()
	X0 = [[ 3, 5 ]]

	Px = np.array([
		[ 0.2, 0 ],
		[ 0, 0.1 ]
	])
	media = kf.obtener_puntos_sigma(X0, Px)
	print(media)