from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên phim")
    description = models.TextField(verbose_name="Mô tả")
    poster = models.URLField(max_length=500, blank=True, verbose_name="URL poster")
    release_year = models.IntegerField(verbose_name="Năm phát hành")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Phim"
        verbose_name_plural = "Phim"
