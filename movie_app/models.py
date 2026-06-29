from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên thể loại")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Thể loại"
        verbose_name_plural = "Thể loại"


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Quốc gia")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Quốc gia"
        verbose_name_plural = "Quốc gia"


class Movie(models.Model):
    class MovieType(models.TextChoices):
        SINGLE = 'single', 'Phim lẻ'
        SERIES = 'series', 'Phim bộ'
        CINEMA = 'cinema', 'Phim chiếu rạp'
        ANIMATION = 'animation', 'Hoạt hình & Anime'

    class Quality(models.TextChoices):
        HD = 'HD', 'HD'
        VIETSUB = 'vietsub', 'Vietsub'
        THUYET_MINH = 'thuyet_minh', 'Thuyết Minh'
        LONG_TIENG = 'long_tieng', 'Lồng Tiếng'

    title = models.CharField(max_length=200, verbose_name="Tên phim")
    title_original = models.CharField(max_length=200, blank=True, verbose_name="Tên gốc")
    description = models.TextField(verbose_name="Mô tả")
    poster = models.URLField(max_length=500, blank=True, verbose_name="URL poster")
    release_year = models.IntegerField(verbose_name="Năm phát hành")
    genres = models.ManyToManyField(Genre, verbose_name="Thể loại")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Quốc gia")
    movie_type = models.CharField(max_length=20, choices=MovieType, default=MovieType.SINGLE, verbose_name="Loại phim")
    quality = models.CharField(max_length=20, choices=Quality, default=Quality.HD, verbose_name="Chất lượng")
    episode_count = models.IntegerField(null=True, blank=True, verbose_name="Số tập")
    is_featured = models.BooleanField(default=False, verbose_name="Phim đề cử")
    views = models.IntegerField(default=0, verbose_name="Lượt xem")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Phim"
        verbose_name_plural = "Phim"
