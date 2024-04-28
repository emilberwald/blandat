import enum
import inspect
import itertools
import sys
import typing
import logging


class NodeMeta(type):
    class Types(enum.Enum):
        BOOLEAN = "BOOLEAN"
        CLIP = "CLIP"
        CLIP_VISION = "CLIP_VISION"
        CLIP_VISION_OUTPUT = "CLIP_VISION_OUTPUT"
        CONDITIONING = "CONDITIONING"
        FLOAT = "FLOAT"
        GLIGEN = "GLIGEN"
        GUIDER = "GUIDER"
        IMAGE = "IMAGE"
        INT = "INT"
        LATENT = "LATENT"
        MASK = "MASK"
        MODEL = "MODEL"
        NOISE = "NOISE"
        PHOTOMAKER = "PHOTOMAKER"
        SAMPLER = "SAMPLER"
        SIGMAS = "SIGMAS"
        STRING = "STRING"
        STYLE_MODEL = "STYLE_MODEL"
        UPSCALE_MODEL = "UPSCALE_MODEL"
        VAE = "VAE"

    @staticmethod
    def int(
        *,
        default=int(),
        minimum=-sys.maxsize - 1,
        maximum=sys.maxsize,
        step=1,
        display: typing.Literal["number", "slider"] = "number",
    ):
        return ("INT", {"default": default, "min": minimum, "max": maximum, "step": step, "display": display})

    @staticmethod
    def float(
        *,
        default=float(),
        minimum=-float("inf"),
        maximum=float("inf"),
        step=1e-2,
        rounding: typing.Optional[float] = None,
        display: typing.Literal["number", "slider"] = "number",
    ):
        return (
            "FLOAT",
            {
                "default": default,
                "min": minimum,
                "max": maximum,
                "step": step,
                "round": rounding,
                "display": display,
            },
        )

    @staticmethod
    def bool(*, default=bool()):
        return ("BOOLEAN", {"default": default})

    @staticmethod
    def str(*, default="", multiline=True, dynamicPrompts=True):
        return (
            "STRING",
            {
                "multiline": multiline,
                "default": default,
            },
        )

    def __new__(
        cls, name, bases, namespace, *, category=__module__, call="__call__", output_node=False, return_names=None
    ) -> type:
        if call in namespace and callable(namespace[call]):
            namespace["CATEGORY"] = category
            namespace["FUNCTION"] = call
            signature = inspect.signature(namespace[call])

            required_variables = dict()
            optional_variables = dict()
            hidden_variables = dict()

            # skip 'self'
            for param_name, param in itertools.islice(signature.parameters.items(), 1, None):
                if typing.get_origin(param.annotation) is typing.Annotated:
                    required_variables[param_name] = cls._handle_input_annotated(param.annotation)
                elif typing.get_origin(param.annotation) is typing.Optional:
                    optional_variables[param_name] = cls._handle_input_param(param)
                else:
                    required_variables[param_name] = cls._to_input_type_hint(param.annotation)

            input_types = {"required": required_variables, "optional": optional_variables, "hidden": hidden_variables}
            logging.info(f"{name}: {signature} => {input_types}")

            namespace["INPUT_TYPES"] = classmethod(lambda cls: input_types)

            namespace["RETURN_TYPES"] = cls._handle_output_signature(signature)
            logging.info(f"{name}: {signature} => {namespace['RETURN_TYPES']}")
            if return_names is not None:
                if len(namespace["RETURN_TYPES"]) == len(return_names):
                    namespace["RETURN_NAMES"] = return_names
            namespace["OUTPUT_NODE"] = output_node

        return super().__new__(cls, name, bases, namespace)

    @classmethod
    def _handle_output_signature(cls, signature):
        if typing.get_origin(signature.return_annotation) is typing.Annotated:
            return_types = cls._handle_output_annotated(signature.return_annotation)
        else:
            return_types = (cls._to_output_type_hint(signature.return_annotation),)
        return return_types

    @classmethod
    def _handle_input_param(cls, param: inspect.Parameter):
        if type_args := typing.get_args(param.annotation):
            for type_arg in type_args:
                if typing.get_origin(type_arg) == typing.Annotated:
                    return cls._handle_input_annotated(type_arg)
                else:
                    return cls._to_output_type_hint(type_arg)

    @classmethod
    def _handle_input_annotated(cls, annotation: typing.Annotated):
        if (type_args := getattr(annotation, "__metadata__", None)) is not None:
            # TODO: support "hidden" here ?
            type_hints = []
            for type_arg in type_args:
                cls._to_input_type_hint(type_arg)
            return tuple(type_hints)

    @classmethod
    def _to_input_type_hint(cls, type_arg):
        if type_arg is float:
            return cls.float()
        elif type_arg is int:
            return cls.int()
        elif type_arg is bool:
            return cls.bool()
        elif type_arg is str:
            return cls.str()
        else:
            return type_arg

    @classmethod
    def _handle_output_annotated(cls, annotation: typing.Annotated):
        if (metadatas := getattr(annotation, "__metadata__", None)) is not None:
            # TODO: support "hidden" here ?
            type_hints = []
            for metadata in metadatas:
                type_hints.append(cls._to_output_type_hint(type_hints, metadata))
            return tuple(type_hints)

    @classmethod
    def _to_output_type_hint(cls, type_arg):
        if type_arg is float:
            return NodeMeta.Types.FLOAT.value
        elif type_arg is int:
            return NodeMeta.Types.INT.value
        elif type_arg is bool:
            return NodeMeta.Types.BOOLEAN.value
        elif type_arg is str:
            return NodeMeta.Types.STRING.value
        else:
            return type_arg
