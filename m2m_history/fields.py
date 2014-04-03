# -*- coding: utf-8 -*-
from django.db import models
from descriptors import ManyRelatedObjectsHistoryDescriptor, ReverseManyRelatedObjectsHistoryDescriptor


class ManyToManyHistoryField(models.ManyToManyField):

    def contribute_to_class(self, cls, name):
        '''
        Call super method and remove unique_together, add time fields and change descriptor class
        '''
        super(ManyToManyHistoryField, self).contribute_to_class(cls, name)

        self.rel.through._meta.unique_together = ()
        self.rel.through.add_to_class('time_from', models.DateTimeField(u'Datetime from', null=True, db_index=True))
        self.rel.through.add_to_class('time_to',  models.DateTimeField(u'Datetime to', null=True, db_index=True))
        # wrong behaviour of south
#        self.rel.through._meta.auto_created = False

        setattr(cls, self.name, ReverseManyRelatedObjectsHistoryDescriptor(self))

    def contribute_to_related_class(self, cls, related):
        '''
        Change descriptor class
        '''
        super(ManyToManyHistoryField, self).contribute_to_related_class(cls, related)

        # `swapped` attribute is not present before Django 1.5
        if not self.rel.is_hidden() and not getattr(related.model._meta, 'swapped', None):
            setattr(cls, related.get_accessor_name(), ManyRelatedObjectsHistoryDescriptor(related))

#     def _get_m2m_db_table(self, opts):
#         db_table = super(ManyToManyHistoryField, self)._get_m2m_db_table(opts)
#         return db_table + '_history'

#     def south_field_triple(self):
#         "Returns a suitable description of this field for South."
#         # We'll just introspect the _actual_ field.
#         from south.modelsinspector import introspector
#         field_class = self.__class__.__module__ + "." + self.__class__.__name__
#         args, kwargs = introspector(self)
#         # That's our definition!
#         print (field_class, args, kwargs)
#         return (field_class, args, kwargs)


# rules = [
#     (
#         (ManyToManyHistoryField,),
#         [],
#         {
#             "to": ["rel.to", {}],
#             "symmetrical": ["rel.symmetrical", {"default": True}],
#             "related_name": ["rel.related_name", {"default": None}],
#             "db_table": ["db_table", {"default": None}],
#             # TODO: Kind of ugly to add this one-time-only option
#             "through": ["rel.through", {"ignore_if_auto_through": True}],
#         },
#     ),
# ]
# from south.modelsinspector import add_introspection_rules
# add_introspection_rules(rules, ["^m2m_history\.fields\.ManyToManyHistoryField"])

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^m2m_history\.fields\.ManyToManyHistoryField"])