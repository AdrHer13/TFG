# from TraceLoader.Interpreter import Interpreter
import json


class TraceLoader:
    current_trace = {}

    def __init__(self):
        return

    def export_to_file(self):
        """
        Función que exporta a formato JSON la variable current_trace
        :return: None
        """

        json_obj = json.dumps(self.current_trace)
        with open('../Traces/game.json', 'w') as outfile:
            outfile.write(json_obj)
        return

    # def import_from_file(self):
    #     """
    #     Función que carga en la variable current_trace un archivo JSON
    #     :return: None
    #     """
    #     with open('../Traces/game.json', 'w') as outfile:
    #         json_obj = outfile.read()
    #
    #     self.current_trace = json.loads(json_obj)
    #     return
