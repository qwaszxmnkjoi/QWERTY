from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import FieldFile


class ModelSerializer(DjangoJSONEncoder):
    def __init__(self, queryset, property_fields: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.property_fields = property_fields or []
        self.queryset = queryset

    def default(self, o):
        if isinstance(o, Model):
            result = self.serialize_obj(o)
        elif isinstance(o, FieldFile):
            result = {
                'url': o.url, 'size': o.size
            } if o else None
            if o and hasattr(o, 'thumbnail'):
                result['thumbnail'] = {'300x300': o.thumbnail['300x300'].url}
        else:
            try:
                result = super().default(o)
            except Exception:
                result = o

        return result

    def as_json(self):
        result = []
        for obj in self.queryset:
            dat = self.serialize_obj(obj) or {}
            if hasattr(obj, 'document'):
                dat.update({'document': ModelSerializer(obj.document.all(), ['file_name', 'file_ext']).as_json()})
            result.append(dat)
        result.reverse()

        return result

    def serialize_obj(self, obj: Model):
        result = {}
        fields = list(obj._meta.local_fields)
        if self.property_fields:
            fields.extend(self.property_fields)
        for fld in fields:
            fld_name = fld if isinstance(fld, str) else fld.name
            dat = getattr(obj, fld_name, None)
            if isinstance(dat, Model):
                dat = self.serialize_obj(dat)
            else:
                dat = self.default(dat)
            result[fld_name] = dat
        return result
