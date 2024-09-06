from app.utils.exceptions import FactoryException


class Factory:
    @classmethod
    def create_subclass(cls, base, prefix, use_base=False, default=False, *args, **kwargs):
        """
        Create a subclass of the given base class.
        """
        uncreated_subclass = cls.get_subclass(base, prefix, use_base, default)

        subclass = uncreated_subclass(*args, **kwargs)

        return subclass

    @classmethod
    def get_subclass(cls, base, prefix, use_base=False, default=False):
        """
        Get the subclass of the given base class, or Base or Default if not found.
        """
        try:
            subs = cls._subclasses(base)
            prefix = prefix.lower().replace("_", "")

            uncreated_subclass = next(
                sub for sub in subs if sub.__name__.lower().startswith(prefix)
            )

        except StopIteration:
            if not use_base and not default:
                raise FactoryException(f"Could not find {base.__name__} for prefix: {prefix}")

            if use_base:
                uncreated_subclass = base

            if default:
                uncreated_subclass = default

        return uncreated_subclass

    @classmethod
    def _subclasses(cls, base):
        """
        Get all subclasses of the given base class.
        """
        classes = []
        for sub in base.__subclasses__():
            classes.append(sub)
            classes.extend(cls._subclasses(sub))
        return classes
