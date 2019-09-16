class NotValidExpandableException(Exception):
    pass


class ModelExpander:

    def solve_expandables(self, elements, expand_args):
        if expand_args:
            result = []
            for q in elements:
                d = q.__dict__.copy()
                del d['_state']
                for expandable in expand_args:
                    exp_list = expandable.split('.')
                    self.expand(q, exp_list, d)
                result.append(d)
            return result
        return elements

    def expand(self, model, expansion_list, d):
        if len(expansion_list) == 0:
            return
        else:
            expandable = expansion_list[0]
            modelproperty = getattr(model, expandable)
            if modelproperty is not None:
                manager = modelproperty._meta.model.objects
                new_model = manager.get(pk=getattr(model,expandable).pk)
                d[expandable] = new_model.__dict__.copy()
                del d[expandable]['_state']
                self.expand(new_model, expansion_list[1:], d[expandable])
        return
