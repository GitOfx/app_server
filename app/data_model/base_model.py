import json

import types
# from sqlalchemy.orm.dynamic import AppenderBaseQuery

class Base_Model:
    def __init__(self, content="success", state=0, data=None, user=None):
        self.content = content
        self.state = state
        self.data = data


class User(Base_Model):
    def __init__(self):
        self.name = "name"
        self.age = 18


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):

        from sqlalchemy.ext.declarative import DeclarativeMeta
        # if isinstance(obj, Base_Model) or isinstance(obj.__class__, DeclarativeMeta) or isinstance(obj, AppenderBaseQuery):
        # an SQLAlchemy class
        fields = {}  # if not x.startswith('_') and x != 'metadata' and x not in ['metadata', 'query', 'query_class']
        for field in [x for x in dir(obj) if
                      not x.startswith('_') and x != 'metadata' and x not in ['metadata', 'query', 'query_class']]:
            try:
                data = obj.__getattribute__(field)   #descriptor '__getattribute__' requires a 'list' object but received a 'str'
                # print("field " + str(field) + " " + str(data))
                if type(data) in [types.CodeType, types.BuiltinFunctionType, types.BuiltinMethodType,
                                  types.FunctionType,
                                  types.MethodType]:
                    continue

                json.dumps(data, ensure_ascii=False,indent=2)  # this will fail on non-encodable values, like other classes
                fields[field] = data
                pass
            except BaseException as e:
                # str1 = str(type(data))
                str2 = "sqlalchemy.orm.dynamic.AppenderBaseQuery"

                # if "AppenderBaseQuery" in str1:
                    # print("``````````sqlalchemy.orm.dynamic.AppenderBaseQuery")
                    # data1 = data.all()
                try:
                    data = obj.__getattribute__(field)
                    json.dumps(data, ensure_ascii=False, cls=AlchemyEncoder,
                               indent=2)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                    pass
                except BaseException as e:
                    fields[field] = None
                    print("field error " + str(field) + " " + str(type(data)))
                    pass



                # else:

                #     print(e)
                #     fields[field] = None
                # print(data)
            # except TypeError as e:
            #     print("field error " + str(field) + " " + str(data))
            #     print(e)
            #     fields[field] = None


        return fields


class exception_model(Base_Model):
    def __init__(self):
        self.content = 'error'
        self.state = '-1'

    def __repr__(self):
        return repr(self.content, self.state)


def toJson(model):
    json_str = json.dumps(model, ensure_ascii=False, cls=AlchemyEncoder, indent=2)
    return json_str


def toModel(json_str):
    model = json.loads(json_str)
    return model


if __name__ == '__main__':
    pass
