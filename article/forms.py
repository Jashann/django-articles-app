# from django import forms
# from tinymce import TinyMCE
# from article.models import Article


# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False


# class ArticleCreateForm(forms.ModelForm):
#     # body = forms.CharField(
#     #     widget=TinyMCEWidget(
#     #         attrs={'required': False, 'cols': 30, 'rows': 10, 'class': 'form-control', 'id': 'mytextarea'}
#     #     )
#     # )
#     class Meta:
#         model = Article
#         fields = ['title', 'cover_image', 'body']
