# from TraceLoader.Interpreter import Interpreter


class TraceLoader:
    current_trace = {}
    # interpreter = Interpreter()

    def __init__(self):
        return

    # def set_trace(self, string):
    #     self.current_trace += string
    #     return
    #
    # def get_trace(self):
    #     return self.current_trace

    def export_to_file(self):
        """
        Función que exporta a formato JSON la variable current_trace
        :return: None
        """
        with open('../Trace/game.json', 'w') as outfile:
            outfile.write(str(self.current_trace))
        return

    def import_to_file(self):
        """
        Función que carga en la variable current_trace un archivo JSON
        :return: None
        """
        return

    def play_trace(self):
        """
        Función que llama a las funciones del intérprete para ejecutar la traza
        :return: None
        """
        return

    def save_to_trace(self):
        """
        TODO
        Función que permite añadir datos a la traza. Requiere de especificar jugador, turno y demás
         o los recogerá automáticamente cuando se le llame
        :return:
        """
        return
