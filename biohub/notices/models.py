from django.conf import settings
from django.db import models


class NoticeQuerySet(models.QuerySet):

    def user_notices(self, user):
        return self.filter(user=user)

    def unread(self):
        return self.filter(has_read=False)

    def mark_read(self):
        return self.update(has_read=True)

    def categories(self):
        return self.order_by('category')\
            .values_list('category', flat=True).distinct()

    def categories_detail(self):
        return self.order_by('category').values('category')\
            .annotate(count=models.Count('id'))\
            .annotate(
                unread=models.ExpressionWrapper(
                    models.F('count') - models.Sum('has_read'),
                    output_field=models.IntegerField()))


class Notice(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notices',
        db_index=True)
    has_read = models.BooleanField(db_index=True, default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    message = models.TextField()
    category = models.CharField(max_length=200, db_index=True)

    objects = NoticeQuerySet.as_manager()

    class Meta:
        ordering = ('-has_read', '-created')

    def mark_read(self):
        self.has_read = True
        self.save()