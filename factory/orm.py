# Copyright: See the LICENSE file.


"""factory_boy extensions for use with orm, https://github.com/encode/orm."""

from factory import base


class OrmModelFactory(base.AsyncFactory):

    class Meta:
        abstract = True  # Optional, but explicit.

    @classmethod
    async def _create_model_async(cls, model_class, *args, **kwargs):
        return await model_class.objects.create(**kwargs)
