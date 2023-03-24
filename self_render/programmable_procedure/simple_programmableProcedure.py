from .programmable_procedure import ProgrammableProcedure


class SimpleProgrammableProcedure(ProgrammableProcedure):
    def __init__(self) -> None:
        super().__init__()
        #
        self._uniform_vars={}
    #
    def set_uniformVar(self, uniform_key,uniform_var):
        self._uniform_vars[uniform_key][None]=uniform_var
    def get_uniformVar(self, uniform_key):
        #assert self._uniform_vars[uniform_key]
        return self._uniform_vars[uniform_key][None]
    def set_uniformBuffer(self, uniform_key,uniform_var):
        self._uniform_vars[uniform_key]=uniform_var
    def get_uniformBuffer(self, uniform_key):
        return self._uniform_vars[uniform_key]
