import enum
import inspect
import itertools
import sys
import typing


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
    def str(*, default="", multiline=True):
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
            for name, param in itertools.islice(signature.parameters.items(), 1, None):
                if typing.get_origin(param.annotation) is typing.Annotated:
                    required_variables[name] = cls._handle_annotated(param.annotation)
                elif typing.get_origin(param.annotation) is typing.Optional:
                    optional_variables[name] = cls._handle_param(param)
                else:
                    raise ValueError(f"{name}: {param}")

            input_types = {"required": required_variables, "optional": optional_variables, "hidden": hidden_variables}
            namespace["INPUT_TYPES"] = classmethod(lambda cls: input_types)

            if typing.get_origin(signature.return_annotation) is typing.Annotated:
                namespace["RETURN_TYPES"] = cls._handle_annotated(signature.return_annotation)
                if return_names is not None:
                    if len(namespace["RETURN_TYPES"]) == len(return_names):
                        namespace["RETURN_NAMES"] = return_names
                namespace["OUTPUT_NODE"] = output_node

        return super().__new__(cls, name, bases, namespace)

    @classmethod
    def _handle_param(cls, param: inspect.Parameter):
        if type_args := typing.get_args(param.annotation):
            for type_arg in type_args:
                if typing.get_origin(type_arg) == typing.Annotated:
                    return cls._handle_annotated(type_arg)

    @classmethod
    def _handle_annotated(cls, annotation: typing.Annotated):
        if (metadatas := getattr(annotation, "__metadata__", None)) is not None:
            # TODO: support "hidden" here ?
            type_hints = []
            for metadata in metadatas:
                if metadata is float:
                    type_hints.append(cls.float())
                elif metadata is int:
                    type_hints.append(cls.int())
                elif metadata is bool:
                    type_hints.append(cls.bool())
                elif metadata is str:
                    type_hints.append(cls.str())
                else:
                    type_hints.append(metadata)
            return tuple(type_hints)
