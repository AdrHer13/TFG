from Classes.Hand import Hand


#
# Interfaz que implementa a un bot
#
class BotInterface:
    resources = Hand()

    # on_trade_offer() -> void
    #
    # Trigger para cuando llega una oferta
    def on_trade_offer(self):
        pass

    # on_turn_start() -> void
    #
    # Trigger para cuando empieza el turno (muy probablemente innecesarios)
    def on_turn_start(self):
        pass

    # on_turn_end() -> void
    #
    # Trigger para cuando acaba el turno (muy probablemente innecesarios)
    def on_turn_end(self):
        pass

    # on_commerce_phase() -> void
    #
    # Trigger para cuando empieza la fase de comercio
    def on_commerce_phase(self):
        pass

    # on_build_phase() -> void
    #
    # Trigger para cuando empieza la fase de construcción
    def on_build_phase(self):
        pass
