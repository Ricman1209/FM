# main.py
from utils.PortadaUtils import generarPortada
from utils.GlosarioUtils import generarGlosario
from utils.SecciónIntroductorioUtils import generarSecciónIntroductoria

def main():
    generarPortada()
    #generarSecciónIntroductoria
    generarGlosario()
    #generarControlCambios
    generarSecciónIntroductoria()
    #generarDiagrama
    #generarÍndice
    print("✅ Portada y glosario generados correctamente.")

if __name__ == "__main__":
    main()
