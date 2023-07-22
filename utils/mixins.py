class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.get_serializer_class)


class SerializerByActionMixin:
    def get_serializer_class(self, *args, **kwargs):
        if hasattr(self, "action"):
            if self.action == "list":
                return self.serializer_map.get("list", self.serializer_class)
            elif self.action == "retrieve":
                return self.serializer_map.get("retrieve", self.serializer_class)
            elif self.action == "create":
                return self.serializer_map.get("create", self.serializer_class)
            elif self.action == "update":
                return self.serializer_map.get("update", self.serializer_class)
            elif self.action == "partial_update":
                return self.serializer_map.get("partial_update", self.serializer_class)
            elif self.action == "destroy":
                return self.serializer_map.get("destroy", self.serializer_class)

        return self.serializer_map.get(self.request.method, self.serializer_class)
