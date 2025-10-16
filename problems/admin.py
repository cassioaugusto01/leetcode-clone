from django.contrib import admin
from .models import Problem, TestCase, Submission, UserProfile


class TestCaseInline(admin.TabularInline):
    """Inline para adicionar casos de teste diretamente na página do problema"""
    model = TestCase
    extra = 1
    fields = ['input_data', 'expected_output', 'is_sample', 'description']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    """Admin para gerenciar desafios"""
    list_display = ['title', 'difficulty', 'created_at', 'get_solved_count']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'description', 'difficulty')
        }),
        ('Configuração de Código', {
            'fields': ('starter_code', 'function_name')
        }),
    )


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    """Admin para gerenciar casos de teste"""
    list_display = ['problem', 'is_sample', 'description']
    list_filter = ['is_sample', 'problem']
    search_fields = ['problem__title', 'description']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin para visualizar submissões"""
    list_display = ['user', 'problem', 'status', 'submitted_at', 'execution_time']
    list_filter = ['status', 'submitted_at', 'problem']
    search_fields = ['user__username', 'problem__title']
    readonly_fields = ['submitted_at', 'execution_time']
    
    def has_add_permission(self, request):
        """Desabilita adição manual de submissões"""
        return False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para visualizar perfis de usuário"""
    list_display = ['user', 'problems_solved', 'total_submissions']
    search_fields = ['user__username']
    readonly_fields = ['problems_solved', 'total_submissions']

