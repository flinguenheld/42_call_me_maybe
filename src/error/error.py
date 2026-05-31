from termcolor import cprint
from pydantic import ValidationError
from typing import Dict, Any, Callable


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀░░
class CallMeError(Exception):
    def __init__(self, message: str, **context: str):
        super().__init__()
        self.context: Dict[str, str] = context

    # ########################################################################
    # ############################################################# PRINT ####
    def print(self) -> None:
        cprint("=============> ERROR <=============", "red", attrs=["blink"])
        for key, val in self.context.items():
            cprint(f"   - {key} ->", "light_red")
            cprint(f"     '{val}'\n", "blue")
        cprint("=============> ERROR <=============", "red", attrs=["blink"])

    def __str__(self) -> str:
        return "\n".join(
            (f"{key} -> {val}" for key, val in self.context.items())
        )

    # ########################################################################
    # ################################################### CATCH DECORATOR ####
    @staticmethod
    def catch(description: str) -> Callable:
        def with_args(func: Callable) -> Callable:
            def inner_func(*args: Any, **kwargs: Any) -> Any:
                try:
                    value = func(*args, **kwargs)
                    return value

                except ValidationError as e:
                    err = e.errors()[0]
                    what = f"Model validation: {err['type']} -> {err['msg']}\n"
                    what += f"""     '{err["loc"]}'\n"""
                    what += f"""     '{err["input"]}'"""
                    raise CallMeError("", what=what, where=description)

                except FileNotFoundError as e:
                    what = "File not found!\n"
                    what += f"     -> '{str(e).split()[7]}'"
                    raise CallMeError("", what=what, where=description)

                except Exception as e:
                    raise CallMeError("", what=str(e), where=description)

            return inner_func

        return with_args
