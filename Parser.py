noterminales = ["S'","S","R","L"]
terminales = ["id", "=", "*"]
#Clase para almacenar el AST
class Nodo:
    def __init__(self, simbolo, hijos=None):
        self.simbolo = simbolo
        self.hijos = hijos or []


def imprimir_ast(nodo, prefijo="", es_ultimo=True, es_raiz=True):
    if es_raiz:
        print(nodo.simbolo)
        nuevo_prefijo = ""
    else:
        print(prefijo + ("   " if es_ultimo else "   ") + nodo.simbolo)
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "    ")
    for i, h in enumerate(nodo.hijos):
        imprimir_ast(h, nuevo_prefijo, i == len(nodo.hijos) - 1, False)

def construir(n, h):
    if n in (1, 3, 5, 6):
        return h[0]
    # 2: S -> L = R
    if n == 2:
        return Nodo("=", [h[0], h[2]])
    # 4: L -> * R
    if n == 4:
        return Nodo("*", [h[1]])
        
def parse(tokens: list):
    tokens = tokens + ["$"]
    pila = [(0, None)] #El segundo parametro guarda el nodo para generar el AST
    i = 0

    while True:
        estado = pila[-1][0]
        token = tokens[i]
        accion = transiciones[estado][simbolos[token]]

        #Si acepta, terminamos
        if accion == "acc":
            return True, pila[-1][1]

        #Cuando solo es un número y esta en no terminales, shift
        if isinstance(accion, int) and accion != 0:
            pila.append((accion, Nodo(token)))
            i += 1

        #Con "rn", reduce
        elif isinstance(accion, str):
            n = int(accion[1:])
            lhs, rhs = producciones[n]
            k = len(rhs)
            #Saca de la pila
            hijos = [nodo for _, nodo in pila[len(pila) - k:]] if k else []
            if k:
                del pila[-k:]
            #Contruimos el ASA
            nodo = construir(n, hijos)
            #Con el nuevo estado transicionado despues de eleminiar
            #Realizamos el movimiento
            destino = transiciones[pila[-1][0]][simbolos[lhs]]
            if destino == 0:
                print(f"Error: goto inválido en estado {pila[-1][0]} con {lhs}")
                return False, None
            pila.append((destino, nodo))

        #Por default, la accion es 0 y es error
        else:
            print(f"Syntax Error: token '{token}' (posición {i}), estado {estado}")
            return False, None
    


if __name__ == "__main__":
    simbolos = {"=":0,"*":1,"id":2,"$":3,"S":4,"L":5,"R":6}

    transiciones = [
    [0,4,5,0,1,2,3],
    [0,0,0,"acc",0,0,0],
    [6,0,0,"r6",0,0,0],
    [0,0,0,"r3",0,0,0],
    [0,4,5,0,0,8,7],
    ["r5",0,0,"r5",0,0,0],
    [0,4,5,0,0,8,9],
    ["r4",0,0,"r4",0,0,0],
    ["r6",0,0,"r6",0,0,0],
    [0,0,0,"r2",0,0,0],
    ]

    producciones = {
    1: ("S'", ["S"]),
    2: ("S",  ["L", "=", "R"]),
    3: ("S",  ["R"]),
    4: ("L",  ["*", "R"]),
    5: ("L",  ["id"]),
    6: ("R",  ["L"]),
    }

    prueba1 = ["id"]
    prueba2 = ["id","=","id"]
    prueba3 = ["*", "id", "=", "id"] #No hay más combinaciones, solo cambiando el id, pero en escencia siempre es el mismo token
    prueba_error1 = ["id", "id"] #Solo ids sin =
    prueba_error2 = ["*", "id", "id"] #falta =
    prueba_error3 = ["*", "id", "="] #Puntero sin id
    prueba_error4 = ["*", "=", "id"] #Falta el id derecho
    prueba_error5 = ["=", "id"] #Falta el id izquierdo


    result1, asa1 = parse(prueba1)
    result2, asa2 = parse(prueba2)
    result3, asa3 = parse(prueba3)

    print(result1)
    imprimir_ast(asa1)
    print("\n"+str(result2))
    imprimir_ast(asa2)
    print("\n"+str(result3))
    imprimir_ast(asa3)

    print("Programas con error: ")
    print(parse(prueba_error1))
    print(parse(prueba_error2))
    print(parse(prueba_error3))
    print(parse(prueba_error4))
    print(parse(prueba_error5))
