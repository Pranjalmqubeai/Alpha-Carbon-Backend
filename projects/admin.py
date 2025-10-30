from django.contrib import admin
from .models import Project, ProjectImage, Impact, Vintage, Document, Transaction

class InlineImage(admin.TabularInline):
    model = ProjectImage
    extra = 0

class InlineImpact(admin.TabularInline):
    model = Impact
    extra = 0

class InlineVintage(admin.TabularInline):
    model = Vintage
    extra = 0

class InlineDoc(admin.TabularInline):
    model = Document
    extra = 0

class InlineTx(admin.TabularInline):
    model = Transaction
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "country", "price", "sdg_score", "created_at")
    search_fields = ("id", "title", "country", "info_company")
    inlines = [InlineImage, InlineImpact, InlineVintage, InlineDoc, InlineTx]
