class ModelExpander:

    def expand(self, model_values_dict, expansion_list):
        if expansion_list[0] not in model_values_dict:
            return
