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
            print(
                f"Could not import {class_name} from {module_name}:",
                exc,
                file=sys.stderr,
            )
            raise
        return clz

    @env.macro
    def pydantic(identifier, key=None):
        from pydantic import BaseModel

        _, class_name = identifier.rsplit(".", 1)
        clz = _load_clz(identifier)
        if not issubclass(clz, BaseModel):
            raise ValueError(f"{class_name} is not a subclass of BaseModel")

        return (
            "### Defaults\n\n"
            + pydantic_example(identifier, key=key, clz=clz)
            + "\n\n### Data model\n\n"
            + pydantic_table(identifier, clz=clz)
        )

    @env.macro
    def pydantic_table(identifier, clz=None, subs=None):
        from pydantic import BaseModel
        from pydantic.fields import UndefinedType, ModelField
        from enum import Enum
        import typing
        import inspect
        import re

        def token_identifier(scanner, token):
            return "IDENTIFIER", token

        def token_lbracket(scanner, token):
            return "LBRACKET", token

        def token_rbracket(scanner, token):
            return "RBRACKET", token

        def token_comma(scanner, token):
            return "COMMA", token

        def token_whitespace(scanner, token):
            return "WHITESPACE", token

        scanner = re.Scanner(
            [
                (r"[a-zA-Z_][a-zA-Z0-9_\.]*", token_identifier),
                (r"\[", token_lbracket),
                (r"\]", token_rbracket),
                (r",", token_comma),
                (r"\s+", token_whitespace),
            ]
        )

        if clz is None:
            clz = _load_clz(identifier)

        if subs is None:
            subs = {}

        def convert_name(name):
            if name.startswith("typing."):
                name = name[len("typing.") :]
            elif name.startswith("typing_extensions."):
                name = name[len("typing_extensions.") :]
            elif name in subs:
                name = subs[name]

            return name

        def convert_enum(enum_):
            bases = [base for base in enum_.__bases__ if not issubclass(base, Enum)]
            if bases:
                return bases[0]
            return enum_

        def type_name(type_):
            if inspect.isclass(type_) and hasattr(type_, "__name__"):
                name = type_.__name__
            else:
                name = str(type_)

            tokens = scanner.scan(name)[0]
            processed = []
            for token in tokens:
                if token[0] == "IDENTIFIER":
                    processed.append(("IDENTIFIER", convert_name(token[1])))
                else:
                    processed.append(token)

            return "".join(token[1] for token in processed)

        def type_doc(type_):
            if inspect.isclass(type_) and issubclass(type_, Enum):
                type_ = convert_enum(type_)
            elif str(type_).startswith("typing.Literal") or str(type_).startswith(
                "typing_extensions.Literal"
            ):
                args = getattr(type_, "__args__")
                if args:
                    type_ = type(args[0])

            name = type_name(type_)

            return f"`{name}`"

        def field_doc(name, field, t):
            type_ = type_doc(t)

            default = getattr(field.field_info, "default", None)
            if isinstance(default, UndefinedType):
                default = "*required*"
            elif default is None:
                default = "*unset*"
            elif isinstance(default, Enum) and convert_enum(t) is not t:
                default = f"`{default.value!r}`"
            else:
                default = f"`{default!r}`"

            description = getattr(field.field_info, "description", None)
            if not description:
                description = ""

            if inspect.isclass(t) and issubclass(t, Enum):
                if convert_enum(t) is not t:
                    choices = [
                        f"`{getattr(t, e).value}`"
                        for e in dir(t)
                        if not e.startswith("_") and hasattr(getattr(t, e), "value")
                    ]
                else:
                    choices = [
                        f"`{getattr(t, e)}`"
                        for e in dir(t)
                        if not e.startswith("_") and hasattr(getattr(t, e), "value")
                    ]

                description += (
                    " " if description else ""
                ) + f"Valid values: {', '.join(choices)}."
            elif str(t).startswith("typing.Literal") or str(t).startswith(
                "typing_extensions.Literal"
            ):
                choices = [f"`{c!r}`" for c in getattr(t, "__args__")]
                description += (
                    " " if description else ""
                ) + f"Valid values: {', '.join(choices)}."

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
