from ruamel.yaml import YAML
from io import StringIO
from typing import Optional, Type


class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


def define_env(env):
    """Hook function"""

    import sys

    src_paths = env.variables.macros_src_paths
    for path in reversed(src_paths):
        sys.path.insert(0, path)

    def _load_clz(identifier: str) -> Optional[Type]:
        import importlib

        module_name, class_name = identifier.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            importlib.reload(module)
            clz = getattr(module, class_name)
        except Exception as exc:
            print(f"Could not import {class_name} from {module_name}:", exc, file=sys.stderr)
            raise
        return clz

    @env.macro
    def version_added(version):
        return f"*New in version {version}.*"

    @env.macro
    def version_changed(version):
        return f"*Changed in version {version}.*"

    @env.macro
    def pydantic(identifier, key=None):
        from pydantic import BaseModel

        _, class_name = identifier.rsplit(".", 1)
        clz = _load_clz(identifier)
        if not issubclass(clz, BaseModel):
            raise ValueError(f"{class_name} is not a subclass of BaseModel")

        return "### Defaults\n\n" + pydantic_example(identifier, key=key, clz=clz) + "\n\n### Data model\n\n" + pydantic_table(identifier, clz=clz)
    
    @env.macro
    def pydantic_table(identifier, clz=None):
        from pydantic import BaseModel
        from pydantic.fields import UndefinedType, ModelField
        from enum import Enum
        import typing
        import inspect

        if clz is None:
            clz = _load_clz(identifier)
        
        def type_doc(type_):
            if inspect.isclass(type_) and issubclass(type_, Enum):
                bases = [base for base in type_.__bases__ if not issubclass(base, Enum)]
                if bases:
                    type_ = bases[0]

            if hasattr(type_, "__name__"):
                type_ = type_.__name__
            type_ = str(type_)
            if type_.startswith("typing."):
                type_ = type_[len("typing."):]
            return f"`{type_}`"

        def field_doc(name, field, t):
            type_ = type_doc(t)

            default = getattr(field.field_info, "default", None)
            if isinstance(default, UndefinedType):
                default = "*required*"
            elif default is None:
                default = "*unset*"
            else:
                default = f"`{default!r}`"
            
            description = getattr(field.field_info, "description", None)
            if not description:
                description = ""
            if inspect.isclass(t) and issubclass(t, Enum):
                choices = [f"`{getattr(t, e)}`" for e in dir(t) if not e.startswith("_")]
                description += (" " if description else "") + f"Valid values: {', '.join(choices)}."
            return f"| `{name}` | {type_} | {description} | {default} |\n"
        
        def model_doc(model, prefix=""):
            result = ""
            type_hints = typing.get_type_hints(model)

            for name, field in model.__fields__.items():
                if isinstance(field, ModelField):
                    alias = field.field_info.alias
                    if alias:
                        name = alias

                if inspect.isclass(field.type_) and issubclass(field.type_, BaseModel):
                    description = field.field_info.description
                    if not description:
                        description = ""
                    
                    type_hint = type_hints.get(name)
                    if inspect.isclass(type_hint) and issubclass(type_hint, BaseModel):
                        result += f"| `{prefix}{name}.*` | | {description} | |\n"
                        result += model_doc(field.type_, prefix=f"{prefix}{name}.")
                    elif str(type_hint).startswith("typing.List"):
                        result += f"| `{prefix}{name}[]` | | {description} | |\n"
                        result += model_doc(field.type_, prefix=f"{prefix}{name}[].")
                else:
                    result += field_doc(prefix + name, field, type_hints.get(name))

            return result
        
        result = ""
        result += f"| Name | Type | Description | Default |\n"
        result += f"| ---- | ---- | ----------- | ------- |\n"
        result += model_doc(clz)
        return result

    @env.macro
    def pydantic_example(identifier, key=None, clz=None, recursive=True):
        from pydantic import BaseModel
        import inspect

        if clz is None:
            clz = _load_clz(identifier)

        yaml = MyYAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.preserve_quotes = True
        yaml.default_flow_style = False

        if inspect.isclass(clz) and issubclass(clz, BaseModel):
            example = clz.construct().dict(by_alias=True)
            if recursive:
                if key:
                    example = {key: example}
                dumped = yaml.dump(example)
                return f"```yaml\n{dumped}\n```\n"
            else:
                result = "```yaml\n"

                prefix = ""
                if key:
                    prefix = "  "
                    result += f"{key}:\n"

                for k in example.keys():
                    result += f"{prefix}{k}:\n{prefix}  # ...\n"
                result += "\n```\n"

                return result

        elif isinstance(clz, list):
            example = []
            for item in clz:
                if isinstance(item, BaseModel):
                    example.append(item.dict(by_alias=True))
                elif isinstance(item, (dict, list, int, float, bool, str)):
                    example.append(item)

            if key:
                example = {key: example}
            dumped = yaml.dump(example)
            return f"```yaml\n{dumped}\n```\n"

        else:
            raise ValueError(f"Don't know how to render {clz}")
