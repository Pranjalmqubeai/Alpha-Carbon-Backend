from rest_framework import serializers
from .models import Project, ProjectImage, Impact, Vintage, Document, Transaction

class ProjectImageSer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["url"]

class ImpactSer(serializers.ModelSerializer):
    class Meta:
        model = Impact
        fields = ["title", "image"]

class VintageSer(serializers.ModelSerializer):
    class Meta:
        model = Vintage
        fields = ["year", "volume", "unit", "price"]

class DocumentSer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["label", "url"]

class TransactionSer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["country", "amount", "units", "date"]

class ProjectSer(serializers.ModelSerializer):
    images = ProjectImageSer(many=True, required=False)
    impacts = ImpactSer(many=True, required=False)
    vintages = VintageSer(many=True, required=False)
    docs = DocumentSer(many=True, required=False)
    transactions = TransactionSer(many=True, required=False)
    sdgs = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Project
        fields = [
            "id", "kind", "title", "country", "country_flag", "price", "sdg_score",
            "thumb", "description", "lat", "lng",
            "info_company","info_address","info_website","info_blockchain","info_type",
            "info_mechanism","info_characteristics","info_registry","info_registry_url",
            "info_validator","info_status","info_credit_start","info_credit_end",
            "sdgs", "images", "impacts", "vintages", "docs", "transactions",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # expose sdgs as list
        if instance.sdgs_csv:
            data["sdgs"] = [int(x) for x in instance.sdgs_csv.split(",") if x]
        else:
            data["sdgs"] = []
        return data

    def _write_children(self, project, data):
        # Clear then bulk-create to keep it simple
        for rel, Model, payload in [
            (project.images, ProjectImage, data.get("images", [])),
            (project.impacts, Impact, data.get("impacts", [])),
            (project.vintages, Vintage, data.get("vintages", [])),
            (project.docs, Document, data.get("docs", [])),
            (project.transactions, Transaction, data.get("transactions", [])),
        ]:
            rel.all().delete()
            objs = [Model(project=project, **item) for item in payload]
            if objs:
                Model.objects.bulk_create(objs)

    def create(self, validated):
        sdgs = validated.pop("sdgs", [])
        images = validated.pop("images", [])
        impacts = validated.pop("impacts", [])
        vintages = validated.pop("vintages", [])
        docs = validated.pop("docs", [])
        transactions = validated.pop("transactions", [])

        project = Project.objects.create(
            **validated,
            sdgs_csv=",".join(str(n) for n in sdgs) if sdgs else ""
        )
        self._write_children(project, {
            "images": images, "impacts": impacts, "vintages": vintages,
            "docs": docs, "transactions": transactions
        })
        return project

    def update(self, instance, validated):
        sdgs = validated.pop("sdgs", None)
        images = validated.pop("images", None)
        impacts = validated.pop("impacts", None)
        vintages = validated.pop("vintages", None)
        docs = validated.pop("docs", None)
        transactions = validated.pop("transactions", None)

        for k, v in validated.items():
            setattr(instance, k, v)
        if sdgs is not None:
            instance.sdgs_csv = ",".join(str(n) for n in sdgs)
        instance.save()

        payload = {}
        if images is not None: payload["images"] = images
        if impacts is not None: payload["impacts"] = impacts
        if vintages is not None: payload["vintages"] = vintages
        if docs is not None: payload["docs"] = docs
        if transactions is not None: payload["transactions"] = transactions
        if payload:
            self._write_children(instance, payload)

        return instance
