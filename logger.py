class Logger:
    def __init__(self, logging_filename):
        self.logging_filename = logging_filename

    def __getattr__(self, key):
        return self.get_parameter(key)

    def get_parameter(self, parameter):
        with open(self.logging_filename, "r") as f:
            searched_value = None
            pars_list = f.read().split("\n")
            for par in pars_list:
                current_par = par.split("=")
                if current_par[0] == parameter:
                    searched_value = current_par[1]
                    break
            return searched_value

    def set_parameter(self, parameter, value):
        with open(self.logging_filename, "r+") as f:
            pars_list = f.read()
            if pars_list.find(parameter) == -1:
                f.write(f"\n{parameter}={value}")
            else:
                pars_list = pars_list.split("\n")
                for par in pars_list:
                    current_par = par.split("=")
                    par_index = pars_list.index(par)
                    if current_par[0] == parameter:
                        current_par[1] = str(value)
                        pars_list[par_index] = "=".join(current_par)
                        break
                f.seek(0)
                f.write("\n".join(pars_list))
