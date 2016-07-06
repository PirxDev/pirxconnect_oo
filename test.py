def DecoradorClienteExiste(funcion):
    def wrapper(arg):
        if arg > 10:
            print("es mayor que 10 no se puede ejecutar")
        else:
            funcion(arg)
    return wrapper


@DecoradorClienteExiste
def suma(numero):
    resultado = numero + 10
    print(resultado)

suma(9)
